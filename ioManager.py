import os
import re
from classes import Coord, GraphicObject3D


class IO:
    def __init__(self, output_path="output", input_path="input"):
        self.output_path = output_path
        self.input_path = input_path

    def import_obj(self):
        with open(self.input_path + "/libraries.mtl", 'r') as f:
            COLORS = {}
            lines = f.readlines()
            i = 0
            newmtl = False
            color = '#'
            while i < len(lines):
                values = lines[i].split(' ')
                if (values[0] == 'newmtl'):
                    newmtl = ' '.join(values[1:]).strip('\n')
                if (values[0] == 'Kd' and newmtl):
                    rgb_values = list(
                        map(lambda x: int(float(x) * 255), values[1:]))
                    color = "#{0:02x}{1:02x}{2:02x}".format(*rgb_values)
                    COLORS[newmtl] = color
                    newmtl = False
                    color = '#'
                i += 1
        f.close()
        with open(self.input_path + "/input.obj", 'r') as f:
            lines = f.readlines()
            i = 0
            coords = []
            name = False
            color = None
            objs = []
            obj_coords = []
            obj_edges = []
            while i < len(lines):
                values = list(filter(lambda x: x != '', lines[i].split(' ')))
                if (values[0] == 'v'):
                    coords.append(
                        Coord(float(values[1]), float(values[2]), float(values[3].strip('\n'))))
                if (values[0] == 'o'):
                    name = values[1].strip('\n')
                    if (len(obj_coords) > 0):
                        objs.append(GraphicObject3D(
                            name, obj_coords, obj_edges, color, None, True))
                        name = False

                    obj_coords = []
                    obj_edges = []
                    color = None
                if (values[0] == 'usemtl'):
                    color = COLORS[' '.join(values[1:]).strip('\n')]
                if (values[0] == 'p'):
                    value = int(values[1])
                    obj_coords.append(
                        coords[value - 1 if value > 0 else value])
                if (values[0] == 'l'):
                    value = list(map(lambda x: int(x.strip('\n')), values[1:]))
                    edge_coords = list(
                        map(lambda y: coords[y - 1 if y > 0 else y], value))
                    edge_index = [len(obj_edges), len(obj_edges) + 1]

                    obj_coords += edge_coords
                    obj_edges.append(edge_index)
                if (values[0] == 'f'):
                    parsed = list(map(int, values[1:-1] +
                                      [values[-1].strip('\n')] + [values[1]]))
                    start_index = len(obj_coords)
                    for j in range(len(values[1:])):
                        eci = [parsed[j], parsed[j+1]]
                        coord_values = list(
                            map(lambda y: coords[y - 1 if y > 0 else y], eci))

                        if (i == 0):
                            obj_coords.append(coord_values[0])

                        obj_coords.append(coord_values[1])

                        obj_coords += coord_values

                        obj_edges.append(
                            [start_index + j, start_index + j + 1])

                        # i = 0
                        # for c in values[1:-1]:
                        #     value = int(c)
                        #     obj_coords.append(
                        #         coords[value - 1 if value > 0 else value])
                        #     edges.appen([i, i+1])
                        #     i += 1
                        # value = int(value[-1].strip('\n'))
                        # obj_coords.append(
                        #     coords[value - 1 if value > 0 else value])
                i += 1
            if (len(obj_coords) > 0):
                objs.append(GraphicObject3D(
                    name, obj_coords, obj_edges, color, None, True))
        f.close()
        return (COLORS, objs)

    def export_obh(self, display_file, colors):
        with open(self.output_path + "/libraries.mtl", 'w') as f:
            for color in colors.items():
                color_tuple = tuple(
                    float(int(color[1].lstrip('#')[i:i+2], 16))/255 for i in (0, 2, 4))
                string = "newmtl " + color[0].upper() + "\n"
                string += "Kd " + str(round(color_tuple[0], 2)) + " " + str(
                    round(color_tuple[1], 2)) + " " + str(round(color_tuple[2], 2)) + "\n"
                f.write(string)
        f.close()
        os.chmod(self.output_path + "/libraries.mtl", 0o777)

        with open(self.output_path + "/output.obj", 'w') as f:
            f.write("mtllib libraries.mtl\n\n")
            coords = []
            for item in display_file:
                range_start = 0 - len(item.coords3d)
                start_index = len(coords)
                for coord in item.coords3d:
                    coords.append(coord)
                    coord_str = "v " + \
                        str(round(coord.x, 2)) + " " + \
                        str(round(coord.y, 2)) + " " + \
                        str(round(coord.z, 2)) + "\n"
                    f.write(coord_str)
                color_name = list(colors.keys())[list(
                    colors.values()).index(item.color)]
                f.write("o " + item.name + "\nusemtl " + color_name + "\n")
                if (item.type == 'point'):
                    f.write("p -1\n")
                else:
                    for edge in item.edges:
                        f.write(
                            "l " + str(edge[0] + start_index) + " " + str(edge[1] + start_index) + '\n')
                f.write("\n\n")
        os.chmod(self.output_path + "/output.obj", 0o777)

        f.close()
