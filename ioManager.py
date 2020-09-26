import os
from classes import Coord, GraphicObject


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
            while i < len(lines):
                values = lines[i].split(' ')
                if (values[0] == 'v'):
                    coords.append(
                        Coord(float(values[1]), float(values[2]), float(values[3].strip('\n'))))
                if (values[0] == 'o'):
                    name = values[1]
                if (values[0] == 'usemtl'):
                    color = COLORS[' '.join(values[1:]).strip('\n')]
                if (values[0] == 'p' or values[0] == 'l' or values[0] == 'f'):
                    if (len(values[1:]) > 2):
                        typeF = None
                        if (values[0] == 'l'):
                            typeF = 'curve'
                        else:
                            typeF = 'polygon'
                    obj_coords = []
                    for c in values[1:]:
                        obj_coords.append(coords[int(c.strip('\n'))])
                    objs.append(GraphicObject(
                        name, obj_coords, color, False, typeF, True))
                    name = False
                    color = None
                i += 1
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
            for item in display_file:
                range_start = 0 - len(item.coords)
                for coord in item.coords:
                    coord_str = "v " + \
                        str(round(coord.x, 2)) + " " + \
                        str(round(coord.y, 2)) + " 0.0\n"
                    f.write(coord_str)
                color_name = list(colors.keys())[list(
                    colors.values()).index(item.color)]
                f.write("o " + item.name + "\nusemtl " + color_name + "\n")
                if (item.type == 'point'):
                    f.write("p -1")
                elif (item.type == 'line' or item.type == 'curve'):
                    string = "l " + \
                        ' '.join(map(str, list(range(range_start, 0))))
                    f.write(string + "\n")
                elif (item.type == 'polygon'):
                    string = "f " + \
                        ' '.join(map(str, list(range(range_start, 0))))
                    f.write(string + "\n")
                f.write("\n\n")
        os.chmod(self.output_path + "/output.obj", 0o777)

        f.close()
