# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from classes import GraphicObject, Coord, Matrix, CalculationMatrix
from popup import Popup
from copy import deepcopy

from ioManager import IO

COLORS = {
    "BLACK": "#000000",
    "RED": "#FF0000",
    "GREEN": "#00FF00",
    "BLUE": "#0000FF",
    "DARK RED": "#880000",
    "DARK GREEN": "#008800",
    "DARK BLUE": "#000088",
    "ORANGE": "#FF8800",
    "LIGHT BLUE": "#0088FF",
    "PINK": "#FF0088",
}


class App:
    def __init__(self):
        # WINDOW CONFIG
        self.root = Tk()
        self.root.title("SGI - Interface grafica para insercao de objetos")
        self.root.geometry("1000x600")
        self.root.state('normal')

        # VARIABLE INITIALIZATION
        self.IO = IO()

        self.display_file = []
        self.display_file_normalized = []
        self.display_file_show = []

        self.labels_x = []
        self.entries_x = []
        self.labels_y = []
        self.entries_y = []

        [colors, objs] = self.IO.import_obj()

        COLORS = colors
        self.display_file = objs

        self.padding = 10

        self.window = GraphicObject("Window", [Coord(0, 0)], COLORS["RED"])
        self.normal_window = GraphicObject("NomalWindow", [
                                           Coord(-1, -1), Coord(1, -1), Coord(1, 1), Coord(-1, 1)], COLORS["RED"])
        self.viewport = GraphicObject(
            "Viewport", [Coord(0, 0)], COLORS["RED"])

        self.window_rotation_angle = 0

        self.height = 0
        self.width = 0

        # RENDER / UPDATE
        self.render()
        self.root.update_idletasks()
        self.canvas_container.update_idletasks()
        self.canvas.update_idletasks()

    def add_curve(self):
        self.add_curve_screen = Toplevel(self.root)
        self.add_curve_screen.title("Selecione o tipo de curva")
        self.add_curve_screen.geometry("300x100")
        buttons_container = Frame(self.add_curve_screen)
        buttons_container.pack(side=TOP, pady=30)
        Button(buttons_container, text="Bezier", command=lambda: self.add_object("curve")).pack(side=LEFT, padx=20)
        Button(buttons_container, text="B-Spline", command=lambda: self.add_object("b_spline_curve")).pack(side=LEFT,padx=20)

    def add_object(self, mode=None):
        if (mode):
            self.add_curve_screen.destroy()
        self.new_object_coords = []
        self.entry_point_destroyed = False
        add_point_text = "Adicionar ponto"
        self.add_object_screen = Toplevel(self.root)
        if (mode):
            self.add_object_screen.title("Adicionar curva")
            self.add_object_screen.geometry("500x500")
            add_point_text = "Adicionar pontos"
        else:
            self.add_object_screen.title("Adicionar objeto")
            self.add_object_screen.geometry("300x400")

        name_object_container = Frame(self.add_object_screen)
        name_object_container.pack(side=TOP)

        self.object_name = StringVar()
        Label(name_object_container, text="Nome do objeto:").pack(side=LEFT)
        Entry(name_object_container,
              textvariable=self.object_name).pack(side=LEFT)

        color_object_container = Frame(
            self.add_object_screen)
        color_object_container.pack(side=TOP)

        Label(color_object_container,
              text="Cor do objeto:").pack(side=LEFT)

        self.color_combobox = ttk.Combobox(
            color_object_container, values=list(COLORS.keys()))
        self.color_combobox.pack(side=LEFT)
        self.color_combobox.current(0)

        entry_container = Frame(self.add_object_screen)
        entry_container.pack(side=TOP, pady=5)

        if (mode == "curve"):
            self.points_x = []
            self.points_y = []
            self.entries_x = []
            self.labels_x = []
            self.entries_y = []
            self.labels_y = []
            for i in range(3):
                self.generate_entry_points(entry_container)
            self.generate_entry_points(entry_container, "removable_point", 0)
        elif (mode == "b_spline_curve"):
            self.points_x = []
            self.points_y = []
            self.entries_x = []
            self.labels_x = []
            self.entries_y = []
            self.labels_y = []
            self.generate_entry_points(entry_container)
            for i in range(3):
                self.generate_entry_points(entry_container, "removable_point", i)
        else:
            entry_x_container = Frame(entry_container)
            entry_x_container.pack(side=TOP)

            entry_y_container = Frame(entry_container)
            entry_y_container.pack(side=TOP)

            self.point_x = IntVar()
            self.point_y = IntVar()
            Label(entry_x_container, text="X").pack(side=LEFT)
            Entry(entry_x_container, textvariable=self.point_x).pack(side=LEFT)
            Label(entry_y_container, text="Y").pack(side=LEFT)
            Entry(entry_y_container, textvariable=self.point_y).pack(side=LEFT)

        buttons_container = Frame(self.add_object_screen)
        self.new_object_listbox = Listbox(buttons_container)

        buttons_container.pack(side=TOP)

        Button(buttons_container, text=add_point_text,
               command=lambda: self.add_point(mode)).pack()
        self.new_object_listbox.pack(pady=5)
        Button(buttons_container, text="Adicionar objeto",
               command=lambda: self.add_object_on_screen(mode)).pack()

    def add_object_on_screen(self, mode):
        if (len(self.object_name.get()) > 0 and len(self.new_object_coords) > 0):
            if (len(self.new_object_coords) >= 3):
                if (mode == "curve"):
                    typeF = "curve"
                elif (mode == "b_spline_curve"):
                    typeF = "b_spline_curve"
                else:
                    typeF = "polygon"
            new_object = GraphicObject(self.object_name.get(
            ), self.new_object_coords, COLORS[self.color_combobox.get()], False, typeF)
            self.listbox.insert(END, new_object.name)
            self.log.insert(0, "Objected " + new_object.name + " added")
            self.display_file.append(new_object)
            self.draw()
            self.add_object_screen.destroy()

    def add_point(self, mode):
        if (mode == "curve" or mode == "b_spline_curve"):
            for i in range(len(self.points_x)):
                x = self.points_x[i].get()
                y = self.points_y[i].get()
                self.new_object_coords.append(Coord(x, y))
                self.new_object_listbox.insert(
                    END, "(" + str(x) + "," + str(y) + ")")
                self.points_x[i].set(0)
                self.points_y[i].set(0)
            if not (self.entry_point_destroyed):
                self.entry_point_destroyed = True
                for i in range(len(self.entries_x)):
                    self.points_x.pop(len(self.points_x) - 1)
                    self.points_y.pop(len(self.points_y) - 1)
                    self.entries_x[i].destroy()
                    self.labels_x[i].destroy()
                    self.entries_y[i].destroy()
                    self.labels_y[i].destroy()
                self.entries_x = []
                self.labels_x = []
                self.entries_y = []
                self.labels_y = []
                # index = len(self.points_x) - 1
                # self.points_x.pop(index)
                # self.points_y.pop(index)
                # self.label_x.destroy()
                # self.entry_x.destroy()
                # self.label_y.destroy()
                # self.entry_y.destroy()
        else:
            x = self.point_x.get()
            y = self.point_y.get()
            self.new_object_coords.append(Coord(x, y))
            self.new_object_listbox.insert(
                END, "(" + str(x) + "," + str(y) + ")")
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
            Coord(XWMIN, YWMIN),
            Coord(XWMIN, YWMAX),
            Coord(XWMAX, YWMAX),
            Coord(XWMAX, YWMIN)
        ]

        self.viewport.coords = [
            Coord(XWMIN + self.padding, YWMIN + self.padding),
            Coord(XWMIN + self.padding, YWMAX - self.padding),
            Coord(XWMAX - self.padding, YWMAX - self.padding),
            Coord(XWMAX - self.padding, YWMIN + self.padding)
        ]

        self.draw()

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
                    if (obj.type == 'polygon'):
                        self.canvas.create_polygon(
                            aux, tags=obj.name, outline=obj.color, fill="")
                    else:
                        self.canvas.create_line(
                            aux, tags=obj.name, fill=obj.color)
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
        self.IO.export_obh(self.display_file, COLORS)

    def generate_scn_matrix(self):
        window_center = self.window.return_center()

        translation_matrix = CalculationMatrix(
            't', [-(window_center.x), -(window_center.y)])
        rotation_matrix = CalculationMatrix('r', self.window_rotation_angle)
        scale_matrix = CalculationMatrix(
            's', [1/(self.get_window_width() / 2), 1/(self.get_window_height() / 2)])

        scn_matrix = translation_matrix * rotation_matrix * scale_matrix
        return scn_matrix

    def generate_entry_points(self, entry_container, mode=None, i=None):
        entry_point_container = Frame(entry_container)
        entry_point_container.pack(side=TOP, pady=2)

        entry_x_container = Frame(entry_point_container)
        entry_x_container.pack(side=LEFT, padx=10)

        entry_y_container = Frame(entry_point_container)
        entry_y_container.pack(side=RIGHT, padx=10)

        point_x = IntVar()
        point_y = IntVar()
        self.points_x.append(point_x)
        self.points_y.append(point_y)

        if (mode == "removable_point"):
            self.labels_x.append(Label(entry_x_container, text="X"))
            self.labels_x[i].pack(side=LEFT)

            self.entries_x.append(Entry(entry_x_container, textvariable=point_x))
            self.entries_x[i].pack(side=LEFT)

            self.labels_y.append(Label(entry_y_container, text="Y"))
            self.labels_y[i].pack(side=LEFT)

            self.entries_y.append(Entry(entry_y_container, textvariable=point_y))
            self.entries_y[i].pack(side=LEFT)
        else:
            Label(entry_x_container, text="X").pack(side=LEFT)
            Entry(entry_x_container, textvariable=point_x).pack(side=LEFT)
            Label(entry_y_container, text="Y").pack(side=LEFT)
            Entry(entry_y_container, textvariable=point_y).pack(side=LEFT)

    def get_canvas_center(self):
        return Coord(self.width / 2, self.height / 2)

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
        return Coord(x, y)

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
            origin = Coord(0, 0)
            if values[3] == 2:
                origin = self.display_file[item].return_center()
            elif values[3] == 3:
                origin = Coord(values[:2])
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
                aux.append(Coord(*result.matrix[0]))
            graphic_object.coords = aux
            graphic_object.normalized = True
            self.display_file_normalized.append(graphic_object)

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

        Label(function_container, text="Funções", width=30).pack(side=TOP)

        self.listbox = Listbox(function_container, width=35, selectmode=SINGLE)
        self.listbox.pack(side=TOP)

        for o in self.display_file:
            self.listbox.insert(END, o.name)

        Button(function_container, width=29, text="Limpar",
               command=self.handle_clear_selection).pack(side=TOP)

        add_and_remove_container = Frame(function_container)
        add_and_remove_container.pack(side=TOP, pady=10)

        curve_container = Frame(function_container)
        curve_container.pack(side=TOP)

        Label(function_container,
              text="Window/Objeto (selecione na listbox)", width=30).pack(side=TOP, pady=10)

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

        Button(curve_container, text="Adicionar curva",
               command=lambda: self.add_curve()).pack(side=BOTTOM)

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
        self.display_file_show = []
        for normalized_object in self.display_file_normalized:
            aux = deepcopy(normalized_object)
            if (len(aux.coords) == 1):
                aux.clip_point()
            elif (len(aux.coords) == 2):
                aux.clip_line()
            elif (len(aux.coords) > 2):
                if (aux.type == 'curve'):
                    aux.clip_curve()
                else:
                    aux.clip_polygon()
            clipped_aux = []
            for obj in aux.clipped:
                clipped_aux.append(self.transform_coords(obj))
            aux.clipped = clipped_aux
            self.display_file_show.append(aux)

    def zoom(self, signal):
        zoom_value = 0.9 if signal > 0 else 1.1
        self.window.center_scale(zoom_value, zoom_value)
        self.log.insert(0, "zoomed in" if signal > 0 else "zoomed out")
        self.draw()
