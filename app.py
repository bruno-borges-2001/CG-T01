from tkinter import *
from tkinter import ttk
from classes import GraphicObject
from popup import Popup

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
        self.root.title("Interface grafica para insercao de objetos")
        self.root.geometry("1000x500")
        self.root.state('normal')

        # VARIABLE INITIALIZATION
        self.objects = []
        self.points = []

        self.left_transform = 0
        self.right_transform = 0
        self.top_transform = 0
        self.bottom_transform = 0

        self.zoom_height = 0
        self.zoom_width = 0

        # RENDER / UPDATE
        self.render()
        self.root.update_idletasks()
        self.canvas_container.update_idletasks()
        self.canvas.update_idletasks()

    def get_canvas_center(self):
        return (self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2)

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
        Button(object_actions_container,
               text="Translação", command=lambda: self.handle_action_click("Translação")).pack(side=LEFT)
        Button(object_actions_container,
               text="Rotação", command=lambda: self.handle_action_click("Rotação")).pack(side=LEFT)
        Button(object_actions_container,
               text="Escala", command=lambda: self.handle_action_click("Escala")).pack(side=LEFT)
        object_actions_container.pack(side=TOP)

        self.canvas_container = Frame(self.root)
        self.canvas_container.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self.canvas_container, background="white")
        self.canvas.pack(fill=BOTH, expand=True)

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

        self.log = Listbox(function_container, width=35)
        self.log.pack(fill=Y, side=BOTTOM)

    def handle_clear_selection(self):
        self.listbox.select_clear(0)

    def draw(self):
        self.canvas.delete("all")
        for i in self.objects:
            tranformed_coords = self.tranform_coords(
                (i.coords + i.coords[:2]) if (len(i.coords) > 4) else i.coords)
            if (len(i.coords) >= 4):
                self.canvas.create_line(
                    tranformed_coords, tags=i.name, fill=i.color)
            else:
                self.canvas.create_oval(
                    tranformed_coords[0] - 1, tranformed_coords[1] - 1, tranformed_coords[0] + 1, tranformed_coords[1] + 1, fill=i.color)

    def handle_translation(self, direction):
        selected = self.listbox.curselection()
        if len(selected) > 0:
            values = self.get_translate_values(direction)
            for item in selected:
                self.log.insert(
                    0, "Object " + self.objects[item].name + " moved " + direction)
                self.objects[item].translate(*values)
            self.draw()
        else:
            self.move_window(direction)

    def handle_zoom(self, signal):
        selected = self.listbox.curselection()
        if len(selected) > 0:
            zoom = 1.1 if signal > 0 else 0.9
            for item in selected:
                self.log.insert(
                    0, "Object " + self.objects[item].name + " zoomed " + ("in" if signal > 0 else "out"))
                self.objects[item].center_scale(zoom, zoom)
            self.draw()
        else:
            self.zoom(signal)

    def get_translate_values(self, direction):
        vertical = self.canvas.winfo_height() * 0.1
        horizontal = self.canvas.winfo_height() * 0.1
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
            self.top_transform += self.canvas.winfo_height() * 0.1
            self.bottom_transform += self.canvas.winfo_height() * 0.1
        elif (direction == 'down'):
            self.top_transform -= self.canvas.winfo_height() * 0.1
            self.bottom_transform -= self.canvas.winfo_height() * 0.1
        elif (direction == 'left'):
            self.left_transform -= self.canvas.winfo_width() * 0.1
            self.right_transform -= self.canvas.winfo_width() * 0.1
        elif (direction == 'right'):
            self.left_transform += self.canvas.winfo_width() * 0.1
            self.right_transform += self.canvas.winfo_width() * 0.1
        self.log.insert(0, "Window moved " + direction)
        self.draw()

    def zoom(self, signal):
        # self.top_transform += signal * self.canvas.winfo_height() * 0.1
        # self.bottom_transform -= signal * self.canvas.winfo_height() * 0.1
        # self.left_transform += signal * self.canvas.winfo_width() * 0.1
        # self.right_transform -= signal * self.canvas.winfo_width() * 0.1

        self.zoom_height += signal * self.canvas_container.winfo_height() * 0.05
        self.zoom_width += signal * self.canvas_container.winfo_width() * 0.05
        self.log.insert(0, "zoomed in" if signal > 0 else "zoomed out")
        self.draw()

    def get_viewport_x(self, xw, xwmin, xwmax, xvpmin, xvpmax):
        return (xw - xwmin) * (xvpmax - xvpmin) / (xwmax - xwmin)

    def get_viewport_y(self, yw, ywmin, ywmax, yvpmin, yvpmax):
        return (1 - ((yw - ywmin) / (ywmax - ywmin))) * (yvpmax - yvpmin)

    def tranform_coords(self, coords):
        aux = []
        XVMIN = 0 - self.zoom_width
        YVMIN = 0 - self.zoom_height
        XVMAX = self.canvas_container.winfo_width() + self.zoom_width
        YVMAX = self.canvas_container.winfo_height() + self.zoom_height

        XWMIN = 0 + self.left_transform
        YWMIN = 0 + self.top_transform
        XWMAX = self.canvas_container.winfo_width() + self.right_transform
        YWMAX = self.canvas_container.winfo_height() + self.bottom_transform

        for i in range(len(coords)):  # ARRAY POS PAR = X / ARRAY POS IMPAR = Y
            coord = coords[i]
            if (i % 2 == 0):
                aux.append(self.get_viewport_x(
                    coord, XWMIN, XWMAX, XVMIN, XVMAX))
            else:
                aux.append(self.get_viewport_y(
                    coord, YWMIN, YWMAX, YVMIN, YVMAX))
        return aux

    def add_object(self):
        # EX DE COORDENADAS => [X1, Y1, X2, Y2, X3, Y3, ..., Xn, Yn]
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
        self.objects.pop(self.listbox.curselection()[0])
        self.listbox.delete(self.listbox.curselection())

    def start_app(self):
        self.root.mainloop()

    def add_point(self):
        x = self.point_x.get()
        y = self.point_y.get()
        self.new_object_coords += [x, y]
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
            self.objects[item].translate(*values[:2])
        elif action == "Rotação":
            origin = (0, 0)
            if values[3] == 2:
                origin = self.objects[item].return_center()
            elif values[3] == 3:
                origin = values[:2]

            angle = values[2]
            self.objects[item].rotate(*origin, angle)
        elif action == "Escala":
            self.objects[item].center_scale(*values[:2])
        self.popup.destroy()
        self.draw()

    def add_object_on_screen(self):
        if (len(self.object_name.get()) > 0 and len(self.new_object_coords) > 0):
            new_object = GraphicObject(
                self.object_name.get(), self.new_object_coords, COLORS[self.color_combobox.get()])
            self.listbox.insert(END, new_object.name)
            self.log.insert(0, "Objected " + new_object.name + " added")
            self.objects.append(new_object)
            self.draw()
            self.add_object_screen.destroy()
