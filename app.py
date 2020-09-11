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

        self.XWMIN = 0
        self.YWMIN = 0
        self.XWMAX = 0
        self.YWMAX = 0

        self.window = GraphicObject("Window", [Coords(0,0)], COLORS["RED"])

        self.window_rotation_direction = "Without Rotation"
        self.window_rotation_angle = 0

        self.left_transform = 0
        self.right_transform = 0
        self.top_transform = 0
        self.bottom_transform = 0

        self.zoom_height = 0
        self.zoom_width = 0

        self.height = 0
        self.width = 0

        # RENDER / UPDATE
        self.render()
        self.root.update_idletasks()
        self.canvas_container.update_idletasks()
        self.canvas.update_idletasks()

    def get_canvas_center(self):
        return Coords(self.width / 2,
                      self.height / 2)

    def get_window_height(self):
        return self.YWMAX - self.YWMIN

    def get_window_width(self):
        return self.XWMAX - self.XWMIN

    def render(self):
        function_container = Frame(self.root, width=30)
        function_container.pack(side=LEFT, fill=Y)

        Label(function_container, text="Funcoes", width=30).pack(side=TOP)

        self.listbox = Listbox(function_container, width=35, selectmode=SINGLE)
        self.listbox.pack(side=TOP)

        Button(function_container, width=29, text="Limpar", command=self.handle_clear_selection
               ).pack(side=TOP)

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

        Button(add_and_remove_container,
               text="Adicionar Objeto", command=self.add_object).pack(side=LEFT)

        Button(add_and_remove_container,
               text="Remover Objeto", command=self.remove_object).pack(side=RIGHT)

        Button(up_container,
               text="↑", command=lambda: self.handle_translation('up')).pack(side=TOP)

        Button(directions_container,
               text="←", command=lambda: self.handle_translation('left')).pack(side=LEFT)

        Button(directions_container,
               text="↓", command=lambda: self.handle_translation('down')).pack(side=LEFT)

        Button(directions_container,
               text="→", command=lambda: self.handle_translation('right')).pack(side=LEFT)

        Button(zoom_container,
               text="+", command=lambda: self.handle_zoom(1)).pack()

        Button(zoom_container,
               text="-", command=lambda: self.handle_zoom(-1)).pack()

        Button(object_actions_container,
               text="Translação", command=lambda: self.handle_action_click("Translação")).pack(side=LEFT)

        Button(object_actions_container,
               text="Rotação", command=lambda: self.handle_action_click("Rotação")).pack(side=LEFT)

        Button(object_actions_container,
               text="Escala", command=lambda: self.handle_action_click("Escala")).pack(side=LEFT)

        Button(rotation_container,
               text="↶", command=lambda: self.handle_window_rotation('left')).pack(side=LEFT)

        Button(rotation_container,
               text="↷", command=lambda: self.handle_window_rotation('right')).pack(side=LEFT)

        self.log = Listbox(function_container, width=35)
        self.log.pack(fill=Y, side=BOTTOM)

    def handle_clear_selection(self):
        self.listbox.select_clear(0, END)

    def check(self, event):
        print(event)
        self.height = self.canvas.winfo_height()
        self.width = self.canvas.winfo_width()

        self.XWMIN = 0 + self.left_transform
        self.YWMIN = 0 + self.top_transform
        self.XWMAX = self.width + self.right_transform
        self.YWMAX = self.height + self.bottom_transform
        coords = [Coords(self.XWMIN, self.YWMIN), Coords(self.XWMIN, self.YWMAX), Coords(self.XWMAX, self.YWMAX), Coords(self.XWMAX, self.YWMIN)]
        self.window.coords = coords
        
        # self.display_file.append(self.window)
        # self.display_file_normalized.append(self.window)
        # self.draw()

    def draw(self):
        self.update_all_points_display_file()
        self.canvas.delete("all")
        for obj in self.display_file_show:
            if (len(obj.coords) >= 2):
                coords = []
                for coord in obj.coords:
                    coords += [coord.x, coord.y]
                coords += [obj.coords[0].x, obj.coords[0].y]
                self.canvas.create_line(coords, tags=obj.name, fill=obj.color)
            else:
                self.canvas.create_oval(
                    obj.coords[0].x - 1, obj.coords[0].y - 1, obj.coords[0].x + 1, obj.coords[0].y + 1, fill=obj.color)

    def update_display_file(self, index, coords):
        self.display_file_normalized[index].coords = self.tranform_coords(
            coords)
        self.display_file_show = self.display_file_normalized

    def update_all_points_display_file(self):
        self.normalize_display_file()
        self.display_file_show = []
        normalized_objects = deepcopy(self.display_file_normalized)
        for normalized_object in normalized_objects:
            normalized_object.coords = self.tranform_coords(normalized_object.coords)
            self.display_file_show.append(normalized_object)

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
        # scn_matrix = self.generate_scn_matrix(direction, 10)
        # graphic_objects = deepcopy(self.display_file)

        # self.display_file_rotation = []
        # for graphic_object in graphic_objects:
        #     aux = []
        #     for coord in graphic_object.coords:
        #         result = CalculationMatrix('c', coord.to_list()) * scn_matrix
        #         aux.append(Coords(*result.matrix[0]))
        #     graphic_object.coords = aux
        #     self.display_file_rotation.append(graphic_object)
        
        self.log.insert(0, "Window rotated " + direction)
        self.draw()
        
    def normalize_display_file(self):
        scn_matrix = self.generate_scn_matrix(self.window_rotation_direction, self.window_rotation_angle)
        graphic_objects = deepcopy(self.display_file)

        self.display_file_normalized = []
        for graphic_object in graphic_objects:
            aux = []
            for coord in graphic_object.coords:
                result = CalculationMatrix('c', coord.to_list()) * scn_matrix
                aux.append(Coords(*result.matrix[0]))
            graphic_object.coords = aux
            self.display_file_normalized.append(graphic_object)

    def generate_scn_matrix(self, direction, angle):
        window_center = self.window.return_center()

        rotation_angle = 0
        if (direction == 'left' ):
            rotation_angle = 360 - angle
        elif (direction == 'right'):
            rotation_angle = angle
        
        translation_matrix = CalculationMatrix('t', [-(window_center.x), -(window_center.y)])
        rotation_matrix = CalculationMatrix('r', rotation_angle)
        scale_matrix = CalculationMatrix('s',[1/(self.get_window_width() / 2), 1/(self.get_window_height() / 2)])
        
        scn_matrix = translation_matrix * rotation_matrix * scale_matrix
        return scn_matrix

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

    def get_translate_values(self, direction):
        vertical = self.height * 0.1
        horizontal = self.width * 0.1
        if (direction == 'up'):
            return (0, vertical)
        elif (direction == 'down'):
            return (0, -vertical)
        elif (direction == 'left'):
            return (-horizontal, 0)
        elif (direction == 'right'):
            return (horizontal, 0)

    def move_window(self, direction):
        if (direction == 'up'):
            self.top_transform += self.height * 0.1
            self.bottom_transform += self.height * 0.1
        elif (direction == 'down'):
            self.top_transform -= self.height * 0.1
            self.bottom_transform -= self.height * 0.1
        elif (direction == 'left'):
            self.left_transform -= self.width * 0.1
            self.right_transform -= self.width * 0.1
        elif (direction == 'right'):
            self.left_transform += self.width * 0.1
            self.right_transform += self.width * 0.1
        self.log.insert(0, "Window moved " + direction)
        self.draw()

    def zoom(self, signal):
        self.zoom_height += signal * self.height * 0.05
        self.zoom_width += signal * self.width * 0.05
        self.log.insert(0, "zoomed in" if signal > 0 else "zoomed out")
        self.draw()

    def get_viewport_coords(self, wcoords, min_wcoords, max_wcoords, min_vpcoords, max_vpcoords):
        x = (wcoords.x - min_wcoords.x) * (max_vpcoords.x - min_vpcoords.x) / (max_wcoords.x - min_wcoords.x)
        y = (1 - ((wcoords.y - min_wcoords.y) / (max_wcoords.y - min_wcoords.y))) * (max_vpcoords.y - min_vpcoords.y)
        return Coords(x, y)

    def tranform_coords(self, coords):
        aux = []
        XVMIN = 0 - self.zoom_width
        YVMIN = 0 - self.zoom_height
        XVMAX = self.width + self.zoom_width
        YVMAX = self.height + self.zoom_height

        self.XWMIN = 0 + self.left_transform
        self.YWMIN = 0 + self.top_transform
        self.XWMAX = self.width + self.right_transform
        self.YWMAX = self.height + self.bottom_transform

        min_wcoords = Coords(self.XWMIN, self.YWMIN)
        max_wcoords = Coords(self.XWMAX, self.YWMAX)
        min_vpcoords = Coords(XVMIN, YVMIN)
        max_vpcoords = Coords(XVMAX, YVMAX)

        for coord in coords:
            aux.append(self.get_viewport_coords(
                coord, min_wcoords, max_wcoords, min_vpcoords, max_vpcoords))
        return aux

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

    def remove_object(self):
        self.log.insert(
            0, "Object " + self.listbox.get(self.listbox.curselection()) + " removed")
        self.canvas.delete(self.listbox.get(self.listbox.curselection()))
        self.display_file.pop(self.listbox.curselection()[0])
        self.listbox.delete(self.listbox.curselection())

    def start_app(self):
        self.root.mainloop()

    def add_point(self):
        x = self.point_x.get()
        y = self.point_y.get()
        self.new_object_coords.append(Coords(x, y))
        self.new_object_listbox.insert(END, "(" + str(x) + "," + str(y) + ")")
        self.point_x.set(0)
        self.point_y.set(0)

    def handle_action_click(self, action):
        selection = self.listbox.curselection()
        if len(selection) > 0:
            self.popup = Popup(
                self.root, action, selection[0], lambda item, values: self.handle_submit(item, action, values))

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

    def add_object_on_screen(self):
        if (len(self.object_name.get()) > 0 and len(self.new_object_coords) > 0):
            new_object = GraphicObject(
                self.object_name.get(), self.new_object_coords, COLORS[self.color_combobox.get()])
            self.listbox.insert(END, new_object.name)
            self.log.insert(0, "Objected " + new_object.name + " added")
            self.display_file.append(new_object)
            # self.display_file_normalized.append(GraphicObject(
            #     self.object_name.get(), self.tranform_coords(self.new_object_coords), COLORS[self.color_combobox.get()]))
            self.display_file_show = self.display_file_normalized
            self.draw()
            self.add_object_screen.destroy()
