import os


class IO:
    def __init__(self, output_path="output", input_path="input"):
        self.output_path = output_path
        self.input_path = input_path

    def import_obj(self):
        with open(self.input_path + "/libraries.mtl", 'r') as f:
          pass

    def export_obh(self, display_file, colors):
        with open(self.output_path + "/libraries.mtl", 'w') as f:
            for color in colors.items():
                color_tuple = tuple(
                    float(int(color[1].lstrip('#')[i:i+2], 16))/255 for i in (0, 2, 4))
                string = "newmtl " + color[0].lower() + "\n"
                string += "Kd " + str(round(color_tuple[0], 2)) + " " + \
                    str(round(color_tuple[1], 2)) + " " + \
                    str(round(color_tuple[2], 2)) + "\n"
                f.write(string)
        f.close()
        os.chmod(self.output_path + "/libraries.mtl", 0o777)

        with open(self.output_path + "/viewport.obj", 'w') as f:
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
                elif (item.type == 'line'):
                    string = "l " + \
                        ' '.join(map(str, list(range(range_start, 0))))
                    f.write(string + "\n")
                elif (item.type == 'polygon'):
                    string = "f " + \
                        ' '.join(map(str, list(range(range_start, 0))))
                    f.write(string + "\n")
                f.write("\n\n")
        os.chmod(self.output_path + "/viewport.obj", 0o777)

        f.close()
