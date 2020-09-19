# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from classes import GraphicObject, Coords, Matrix, CalculationMatrix
from popup import Popup
from copy import deepcopy

COLORS = {
    "BLACK": "#000",
    "RED": "#F00",
    "GREEN": "#0F0",
    "BLUE": "#00F",
    "DARK RED": "#800",
    "DARK GREEN": "#080",
    "DARK BLUE": "#008",
    "ORANGE": "#F80",
    "LIGHT BLUE": "#08F",
    "PINK": "#F08",
}


class App:
    def __init__(self):
        # WINDOW CONFIG
        self.root = Tk()
        self.root.title("SGI - Interface grafica para insercao de objetos")
        self.root.geometry("1000x600")
        self.root.state('normal')

        # VARIABLE INITIALIZATION
        self.display_file = []
        self.display_file_normalized = []
        self.display_file_show = []

        self.padding = 10

        self.window = GraphicObject("Window", [Coords(0, 0)], COLORS["RED"])
        self.normal_window = GraphicObject("NomalWindow", [
                                           Coords(-1, -1), Coords(1, -1), Coords(1, 1), Coords(-1, 1)], COLORS["RED"])
        self.viewport = GraphicObject(
            "Viewport", [Coords(0, 0)], COLORS["RED"])

        self.window_rotation_angle = 0

        self.height = 0
        self.width = 0

        # RENDER / UPDATE
        self.render()
        self.root.update_idletasks()
        self.canvas_container.update_idletasks()
        self.canvas.update_idletasks()

    def add_object(self):
        self.new_object_coords = []

        self.add_object_screen = Toplevel(self.root)
        self.add_object_screen.title("Adicionar objeto")
        self.add_object_screen.geometry("300x400")

        self.name_object_container = Frame(self.add_object_screen)
        self.name_object_container.pack(side=TOP)

        self.object_name = StringVar()
        Label(self.name_object_container, text="Nome do objeto:").pack(side=LEFT)
        Entry(self.name_object_container,
              textvariable=self.object_name).pack(side=LEFT)

        self.color_object_container = Frame(
            self.add_object_screen)
        self.color_object_container.pack(side=TOP)

        Label(self.color_object_container,
              text="Cor do objeto:").pack(side=LEFT)

        self.color_combobox = ttk.Combobox(
            self.color_object_container, values=list(COLORS.keys()))
        self.color_combobox.pack(side=LEFT)
        self.color_combobox.current(0)

        entry_container = Frame(self.add_object_screen)
        entry_container.pack(side=TOP, pady=5)

        entry_x_container = Frame(entry_container)
        entry_x_container.pack(side=TOP)

        entry_y_container = Frame(entry_container)
        entry_y_container.pack(side=TOP)
        self.buttons_container = Frame(self.add_object_screen)
        self.new_object_listbox = Listbox(self.buttons_container)

        self.point_x = IntVar()
        self.point_y = IntVar()
        Label(entry_x_container, text="X").pack(side=LEFT)
        Entry(entry_x_container, textvariable=self.point_x).pack(side=LEFT)
        Label(entry_y_container, text="Y").pack(side=LEFT)
        Entry(entry_y_container, textvariable=self.point_y).pack(side=LEFT)

        self.buttons_container.pack(side=TOP)

        Button(self.buttons_container, text="Adicionar ponto",
               command=self.add_point).pack()
        self.new_object_listbox.pack(pady=5)
        Button(self.buttons_container, text="Adicionar objeto",
               command=self.add_object_on_screen).pack()

    def add_object_on_screen(self):
        if (len(self.object_name.get()) > 0 and len(self.new_object_coords) > 0):
            new_object = GraphicObject(
                self.object_name.get(), self.new_object_coords, COLORS[self.color_combobox.get()])
            self.listbox.insert(END, new_object.name)
            self.log.insert(0, "Objected " + new_object.name + " added")
            self.display_file.append(new_object)
            self.draw()
            self.add_object_screen.destroy()

    def add_point(self):
        x = self.point_x.get()
        y = self.point_y.get()
        self.new_object_coords.append(Coords(x, y))
        self.new_object_listbox.insert(END, "(" + str(x) + "," + str(y) + ")")
        self.point_x.set(0)
        self.point_y.set(0)

    def check(self, event):
        self.height = self.canvas.winfo_height()
        self.width = self.canvas.winfo_width()

        XWMIN = 0
        YWMIN = 0
        XWMAX = self.width
        YWMAX = self.height

        self.window.coords = [
            Coords(XWMIN, YWMIN),
            Coords(XWMIN, YWMAX),
            Coords(XWMAX, YWMAX),
            Coords(XWMAX, YWMIN)
        ]

        self.viewport.coords = [
            Coords(XWMIN + self.padding, YWMIN + self.padding),
            Coords(XWMIN + self.padding, YWMAX - self.padding),
            Coords(XWMAX - self.padding, YWMAX - self.padding),
            Coords(XWMAX - self.padding, YWMIN + self.padding)
        ]

        self.draw()

    def clipping(self):
        self.display_file_show = []
        for normalized_object in self.display_file_normalized:
            if (len(normalized_object.coords) == 1):
                self.point_clipping(normalized_object)
            elif (len(normalized_object.coords) == 2):
                self.line_clipping(normalized_object)
            else:
                self.polygon_clipping(normalized_object)

    def draw(self):
        self.update_all_points_display_file()
        self.canvas.delete("all")
        aux = []
        for coord in self.viewport.coords:
            aux += coord.to_list()[:-1]
        self.canvas.create_polygon(
            aux, tags="viewport", outline=self.viewport.color, fill="")
        for obj in self.display_file_show:
            for coords in obj.clipped:
                if (len(coords) > 2):
                    aux = []
                    for coord in coords:
                        aux += [coord.x + self.padding,
                                coord.y + self.padding]
                    self.canvas.create_polygon(
                        aux, tags=obj.name, outline=obj.color, fill="")
                elif (len(coords) == 2):
                    aux = []
                    for coord in coords:
                        aux += [coord.x + self.padding,
                                coord.y + self.padding]
                    self.canvas.create_line(
                        aux, tags=obj.name, fill=obj.color)
                elif (len(coords) == 1):
                    self.canvas.create_oval(
                        coords[0].x - 1 + self.padding, coords[0].y - 1 + self.padding, coords[0].x + 1 + self.padding, coords[0].y + 1 + self.padding, fill=obj.color)
        self.canvas.tag_raise("viewport")

    def generate_scn_matrix(self):
        window_center = self.window.return_center()

        translation_matrix = CalculationMatrix(
            't', [-(window_center.x), -(window_center.y)])
        rotation_matrix = CalculationMatrix('r', self.window_rotation_angle)
        scale_matrix = CalculationMatrix(
            's', [1/(self.get_window_width() / 2), 1/(self.get_window_height() / 2)])

        scn_matrix = translation_matrix * rotation_matrix * scale_matrix
        return scn_matrix

    def get_canvas_center(self):
        return Coords(self.width / 2, self.height / 2)

    def get_window_height(self):
        return self.window.coords[2].y - self.window.coords[0].y

    def get_window_width(self):
        return self.window.coords[2].x - self.window.coords[0].x

    def get_translate_values(self, direction):
        value = self.get_window_height() * 0.1
        if (direction == 'up'):
            return (0, value)
        elif (direction == 'down'):
            return (0, -value)
        elif (direction == 'left'):
            return (-value, 0)
        elif (direction == 'right'):
            return (value, 0)

    def get_viewport_coords(self, wcoords):
        min_wcoords = self.normal_window.coords[0]
        max_wcoords = self.normal_window.coords[2]
        min_vpcoords = self.viewport.coords[0]
        max_vpcoords = self.viewport.coords[2]
        x = (wcoords.x - min_wcoords.x) * (max_vpcoords.x -
                                           min_vpcoords.x) / (max_wcoords.x - min_wcoords.x)
        y = (1 - ((wcoords.y - min_wcoords.y) / (max_wcoords.y -
                                                 min_wcoords.y))) * (max_vpcoords.y - min_vpcoords.y)
        return Coords(x, y)

    def handle_action_click(self, action):
        selection = self.listbox.curselection()
        if len(selection) > 0:
            self.popup = Popup(
                self.root, action, selection[0], lambda item, values: self.handle_submit(item, action, values))

    def handle_clear_selection(self):
        self.listbox.select_clear(0, END)

    def handle_submit(self, item, action, values):
        if action == "Translação":
            self.display_file[item].translate(*values[:2])
        elif action == "Rotação":
            origin = Coords(0, 0)
            if values[3] == 2:
                origin = self.display_file[item].return_center()
            elif values[3] == 3:
                origin = Coords(values[:2])
            angle = values[2]
            self.display_file[item].rotate(origin.x, origin.y, angle)
        elif action == "Escala":
            self.display_file[item].center_scale(*values[:2])
        self.popup.destroy()
        self.draw()

    def handle_translation(self, direction):
        selected = self.listbox.curselection()
        if len(selected) > 0:
            values = self.get_translate_values(direction)
            for item in selected:
                self.log.insert(
                    0, "Object " + self.display_file[item].name + " moved " + direction)
                self.display_file[item].translate(*values)
            self.draw()
        else:
            self.move_window(direction)

    def handle_window_rotation(self, direction):
        self.window_rotation_angle += 15 if direction == 'right' else -15

        self.log.insert(0, "Window rotated " + direction)
        self.draw()

    def handle_zoom(self, signal):
        selected = self.listbox.curselection()
        if len(selected) > 0:
            zoom = 1.1 if signal > 0 else 0.9
            for item in selected:
                self.log.insert(
                    0, "Object " + self.display_file[item].name + " zoomed " + ("in" if signal > 0 else "out"))
                self.display_file[item].center_scale(zoom, zoom)
            self.draw()
        else:
            self.zoom(signal)

    def line_clipping(self, graphic_object):
        clipped_line = GraphicObject(
            graphic_object.name, graphic_object.coords, graphic_object.color)

        min_wcoords = self.normal_window.coords[0]
        max_wcoords = self.normal_window.coords[2]

        xl = min_wcoords.x
        xr = max_wcoords.x
        yb = min_wcoords.y
        yt = max_wcoords.y
        # setting region codes of the coordinates of each point
        points_region_codes = []
        for coord in graphic_object.coords:
            region_code = int('0000', 2)
            if (coord.x < xl):
                region_code = region_code | int('0001', 2)
            if (coord.x > xr):
                region_code = region_code | int('0010', 2)
            if (coord.y < yb):
                region_code = region_code | int('0100', 2)
            if (coord.y > yt):
                region_code = region_code | int('1000', 2)
            points_region_codes.append(region_code)

        # checking position of points
        rc1 = points_region_codes[0]
        rc2 = points_region_codes[1]
        if (rc1 == 0 and rc2 == 0):
            self.display_file_show.append(graphic_object)
        elif (rc1 & rc2 != 0):
            pass
        elif (rc1 & rc2 == 0 and rc1 != rc2):
            p1 = graphic_object.coords[0]
            p2 = graphic_object.coords[1]

            m = (p2.y - p1.y) / (p2.x - p1.x)

            # checks if the line intersects the window
            intersects = True
            rc_intersects = False
            for i in range(len(points_region_codes)):
                if (intersects):
                    rc = points_region_codes[i]
                    if (rc & int('0001', 2) == int('0001', 2)):  # left intersection
                        y = m * (xl - p1.x) + p1.y
                        if (y >= yb and y <= yt):
                            rc_intersects = True
                            clipped_line.coords[i].x = xl
                            clipped_line.coords[i].y = y
                        else:
                            intersects = rc_intersects
                    if (rc & int('0010', 2) == int('0010', 2)):  # right intersection
                        y = m * (xr - p1.x) + p1.y
                        if (y >= yb and y <= yt):
                            rc_intersects = True
                            clipped_line.coords[i].x = xr
                            clipped_line.coords[i].y = y
                        else:
                            intersects = rc_intersects
                    if (rc & int('0100', 2) == int('0100', 2)):  # bottom intersection
                        x = p1.x + (1/m) * (yb - p1.y)
                        if (x >= xl and x <= xr):
                            rc_intersects = True
                            clipped_line.coords[i].x = x
                            clipped_line.coords[i].y = yb
                        else:
                            intersects = rc_intersects
                    if (rc & int('1000', 2) == int('1000', 2)):  # top intersection
                        x = p1.x + (1/m) * (yt - p1.y)
                        if (x >= xl and x <= xr):
                            rc_intersects = True
                            clipped_line.coords[i].x = x
                            clipped_line.coords[i].y = yt
                        else:
                            intersects = rc_intersects
            if (intersects):
                self.display_file_show.append(clipped_line)

    def move_window(self, direction):
        Cx = 0
        Cy = 0
        if (direction == 'up'):
            Cy = self.get_window_height() * 0.1
        elif (direction == 'down'):
            Cy = -self.get_window_height() * 0.1
        elif (direction == "left"):
            Cx = -self.get_window_height() * 0.1
        elif (direction == 'right'):
            Cx = self.get_window_height() * 0.1
        self.window.translate(Cx, Cy)
        self.log.insert(0, "Window moved " + direction)
        self.draw()

    def normalize_display_file(self):
        scn_matrix = self.generate_scn_matrix()
        graphic_objects = deepcopy(self.display_file)

        self.display_file_normalized = []
        for graphic_object in graphic_objects:
            aux = []
            for coord in graphic_object.coords:
                result = CalculationMatrix('c', coord.to_list()) * scn_matrix
                aux.append(Coords(*result.matrix[0]))
            graphic_object.coords = aux
            graphic_object.normalized = True
            self.display_file_normalized.append(graphic_object)

    def point_clipping(self, graphic_object):
        min_wcoords = self.normal_window.coords[0]
        max_wcoords = self.normal_window.coords[2]
        if (graphic_object.coords[0].x >= min_wcoords.x and graphic_object.coords[0].x <= max_wcoords.x):
            if (graphic_object.coords[0].y >= min_wcoords.y and graphic_object.coords[0].y <= max_wcoords.y):
                self.display_file_show.append(graphic_object)

    def polygon_clipping(self, graphic_object):
        clipped_polygon = GraphicObject(
            graphic_object.name, graphic_object.coords, graphic_object.color)

        min_wcoords = self.normal_window.coords[0]
        max_wcoords = self.normal_window.coords[2]
        pass

    def remove_object(self):
        self.log.insert(
            0, "Object " + self.listbox.get(self.listbox.curselection()) + " removed")
        self.canvas.delete(self.listbox.get(self.listbox.curselection()))
        self.display_file.pop(self.listbox.curselection()[0])
        self.listbox.delete(self.listbox.curselection())
        self.draw()

    def render(self):
        function_container = Frame(self.root, width=30)
        function_container.pack(side=LEFT, fill=Y)

        Label(function_container, text="Funcoes", width=30).pack(side=TOP)

        self.listbox = Listbox(function_container, width=35, selectmode=SINGLE)
        self.listbox.pack(side=TOP)

        Button(function_container, width=29, text="Limpar",
               command=self.handle_clear_selection).pack(side=TOP)

        add_and_remove_container = Frame(function_container)
        add_and_remove_container.pack(side=TOP, pady=10)

        Label(function_container,
              text="Window/Objeto (selecione na listbox)", width=30).pack(side=TOP)

        main_button_container = Frame(function_container, width=35)
        main_button_container.pack(side=TOP)

        arrows_container = Frame(main_button_container, padx=10)
        arrows_container.pack(side=LEFT)

        up_container = Frame(arrows_container)
        up_container.pack(side=TOP)

        directions_container = Frame(arrows_container)
        directions_container.pack(side=TOP)

        zoom_container = Frame(main_button_container)
        zoom_container.pack(side=RIGHT, pady=10, padx=10)

        object_actions_container = Frame(function_container)
        object_actions_container.pack(side=TOP)

        rotation_container = Frame(function_container)
        rotation_container.pack(side=TOP, pady=10)

        self.canvas_container = Frame(self.root)
        self.canvas_container.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self.canvas_container, background="white")
        self.canvas.pack(fill=BOTH, expand=True)

        self.canvas.bind("<Configure>", self.check)

        Button(add_and_remove_container, text="Adicionar Objeto",
               command=self.add_object).pack(side=LEFT)

        Button(add_and_remove_container, text="Remover Objeto",
               command=self.remove_object).pack(side=RIGHT)

        Button(up_container, text="↑",
               command=lambda: self.handle_translation('up')).pack(side=TOP)

        Button(directions_container, text="←",
               command=lambda: self.handle_translation('left')).pack(side=LEFT)

        Button(directions_container, text="↓",
               command=lambda: self.handle_translation('down')).pack(side=LEFT)

        Button(directions_container, text="→",
               command=lambda: self.handle_translation('right')).pack(side=LEFT)

        Button(zoom_container, text="+",
               command=lambda: self.handle_zoom(1)).pack()

        Button(zoom_container, text="-",
               command=lambda: self.handle_zoom(-1)).pack()

        Button(object_actions_container, text="Translação",
               command=lambda: self.handle_action_click("Translação")).pack(side=LEFT)

        Button(object_actions_container, text="Rotação",
               command=lambda: self.handle_action_click("Rotação")).pack(side=LEFT)

        Button(object_actions_container, text="Escala",
               command=lambda: self.handle_action_click("Escala")).pack(side=LEFT)

        Button(rotation_container, text="↶",
               command=lambda: self.handle_window_rotation('left')).pack(side=LEFT)

        Button(rotation_container, text="↷",
               command=lambda: self.handle_window_rotation('right')).pack(side=LEFT)

        self.log = Listbox(function_container, width=35)
        self.log.pack(fill=Y, side=BOTTOM)

    def start_app(self):
        self.root.mainloop()

    def transform_coords(self, coords):
        aux = []
        for coord in coords:
            aux.append(self.get_viewport_coords(coord))
        return aux

    def update_all_points_display_file(self):
        self.normalize_display_file()
        # self.clipping()
        self.display_file_show = []
        for normalized_object in self.display_file_normalized:
            # for normalized_object in self.display_file_show:
            aux = deepcopy(normalized_object)
            if (len(aux.coords) == 1):
                aux.clip_point()
            elif (len(aux.coords) == 2):
                aux.clip_line()
            elif (len(aux.coords) > 2):
                aux.clip_polygon()
            clipped_aux = []
            for obj in aux.clipped:
                clipped_aux.append(self.transform_coords(obj))
            aux.clipped = clipped_aux
            self.display_file_show.append(aux)

            # normalized_object.coords = self.transform_coords(
            #     normalized_object.coords)

    def zoom(self, signal):
        zoom_value = 0.9 if signal > 0 else 1.1
        self.window.center_scale(zoom_value, zoom_value)
        self.log.insert(0, "zoomed in" if signal > 0 else "zoomed out")
        self.draw()
