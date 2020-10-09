from tkinter import *
from tkinter import ttk

from classes import Coord


class TransformationPopup:

    def __init__(self, parent, option, item, on_submit):
        self.root = Toplevel(parent)
        self.root.title(option)
        self.root.geometry("300x200")
        self.option = option

        self.x_value = DoubleVar()
        self.y_value = DoubleVar()
        self.angle = DoubleVar()

        self.rotation_type = IntVar()

        self.submit_function = on_submit

        self.container = False

        self.item = item

        self.render()

    def render(self):
        Label(self.root, text=self.option).pack(side=TOP)

        if (self.option == "Rotação"):
            angle_entry = Frame(self.root)
            Label(angle_entry, text="Ângulo:").pack(side=LEFT)
            Entry(angle_entry, textvariable=self.angle).pack(side=LEFT)
            angle_entry.pack(side=TOP)
            radio_container = Frame(self.root)
            Radiobutton(radio_container, text="Mundo",
                        variable=self.rotation_type, value=1, command=self.render_coords).pack(side=LEFT)
            Radiobutton(radio_container, text="Objeto",
                        variable=self.rotation_type, value=2, command=self.render_coords).pack(side=LEFT)
            Radiobutton(radio_container, text="Coordenada",
                        variable=self.rotation_type, value=3, command=self.render_coords).pack(side=LEFT)
            radio_container.pack(side=TOP)

        self.render_coords()

        submit_button = Button(self.root, text="Executar ação",
                               command=lambda: self.submit_function(self.item, [self.x_value.get(), self.y_value.get(), self.angle.get(), self.rotation_type.get()]))
        submit_button.pack(side=BOTTOM, pady=5)

    def render_coords(self):
        if (self.container and self.option == "Rotação"):
            self.container.destroy()

        self.container = Frame(self.root)

        if (self.option != "Rotação" or self.rotation_type.get() == 3):
            Label(self.container, text="Vetor" if self.option !=
                  "Rotação" else "Origem")
            Label(self.container, text="x").pack(side=LEFT)
            Entry(self.container, textvariable=self.x_value).pack(side=LEFT)
            Label(self.container, text="y").pack(side=LEFT)
            Entry(self.container,
                  textvariable=self.y_value).pack(side=LEFT)
            self.container.pack(side=TOP)

    def destroy(self):
        self.root.destroy()


class Object2DPopup:
    def __init__(self, parent, on_submit, colors):
        self.new_object_coords = []
        self.root = Toplevel(parent)
        self.root.title("Adicionar objeto")
        self.root.geometry("300x400")

        self.on_submit = on_submit

        name_object_container = Frame(self.root)
        name_object_container.pack(side=TOP)

        self.object_name = StringVar()
        Label(name_object_container, text="Nome do objeto:").pack(side=LEFT)
        Entry(name_object_container,
              textvariable=self.object_name).pack(side=LEFT)

        color_object_container = Frame(self.root)
        color_object_container.pack(side=TOP)

        Label(color_object_container,
              text="Cor do objeto:").pack(side=LEFT)

        self.color_combobox = ttk.Combobox(
            color_object_container, values=list(colors.keys()))
        self.color_combobox.pack(side=LEFT)
        self.color_combobox.current(0)

        entry_container = Frame(self.root)
        entry_container.pack(side=TOP, pady=5)

        entry_x_container = Frame(entry_container)
        entry_x_container.pack(side=TOP)

        entry_y_container = Frame(entry_container)
        entry_y_container.pack(side=TOP)

        self.point_x = DoubleVar()
        self.point_y = DoubleVar()
        Label(entry_x_container, text="X").pack(side=LEFT)
        Entry(entry_x_container, textvariable=self.point_x).pack(side=LEFT)
        Label(entry_y_container, text="Y").pack(side=LEFT)
        Entry(entry_y_container, textvariable=self.point_y).pack(side=LEFT)

        buttons_container = Frame(self.root)
        self.new_object_listbox = Listbox(buttons_container)

        buttons_container.pack(side=TOP)

        Button(buttons_container, text="Adicionar Ponto",
               command=self.add_point).pack()
        self.new_object_listbox.pack(pady=5)

        self.new_object_type = IntVar()
        self.new_object_type.set(-1)

        radio_container = Frame(buttons_container)
        top_container = Frame(radio_container)
        bottom_container = Frame(radio_container)

        top_container.pack(side=TOP)
        bottom_container.pack(side=BOTTOM)
        self.radio_buttons = [Radiobutton(top_container, text="Ponto",
                                          variable=self.new_object_type, value=0),
                              Radiobutton(top_container, text="Linha",
                                          variable=self.new_object_type, value=1),
                              Radiobutton(top_container, text="Curva (Bezier)",
                                          variable=self.new_object_type, value=2),
                              Radiobutton(bottom_container, text="Curva (B-Spline)",
                                          variable=self.new_object_type, value=3),
                              Radiobutton(bottom_container, text="Polígono",
                                          variable=self.new_object_type, value=4)]

        for rb in self.radio_buttons:
            rb.pack(side=LEFT)

            rb.configure(state=DISABLED)

        radio_container.pack(side=TOP)

        Button(buttons_container, text="Adicionar objeto",
               command=self.add_object_on_screen).pack()

    def add_object_on_screen(self):
        self.on_submit(self.new_object_type.get(),
                       self.object_name.get(), self.new_object_coords, self.color_combobox.get())

    def add_point(self):
        x = self.point_x.get()
        y = self.point_y.get()
        self.new_object_coords.append(Coord(x, y))
        self.new_object_listbox.insert(
            END, "(" + str(x) + "," + str(y) + ")")
        self.point_x.set(0)
        self.point_y.set(0)

        self.configureRadioButtons()

    def configureRadioButtons(self):
        self.new_object_type.set(-1)
        for rb in self.radio_buttons:
            rb.configure(state=DISABLED)
        length = len(self.new_object_coords)
        if (length == 1):
            self.radio_buttons[0].configure(state=ACTIVE)
        elif (length == 2):
            self.radio_buttons[1].configure(state=ACTIVE)
        elif (length == 3):
            self.radio_buttons[1].configure(state=ACTIVE)
            self.radio_buttons[4].configure(state=ACTIVE)
        elif (length >= 4):
            self.radio_buttons[1].configure(state=ACTIVE)
            self.radio_buttons[3].configure(state=ACTIVE)
            self.radio_buttons[4].configure(state=ACTIVE)
            aux = length - 4
            if (aux % 3 == 0):
                self.radio_buttons[2].configure(state=ACTIVE)

    def destroy(self):
        self.root.destroy()


class Object3DPopup:
    def __init__(self, parent, on_submit, colors):
        self.root = Toplevel(parent)
        self.root.title('Criar Objeto 3d')
        self.root.geometry("600x700")

        self.on_submit = on_submit

        self.coords = []
        self.edges = []

        self.new_object_coords = []

        name_object_container = Frame(self.root)
        name_object_container.pack(side=TOP)

        self.object_name = StringVar()
        Label(name_object_container, text="Nome do objeto:").pack(side=LEFT)
        Entry(name_object_container,
              textvariable=self.object_name).pack(side=LEFT)

        color_object_container = Frame(self.root)
        color_object_container.pack(side=TOP)

        Label(color_object_container,
              text="Cor do objeto:").pack(side=LEFT)

        self.color_combobox = ttk.Combobox(
            color_object_container, values=list(colors.keys()))
        self.color_combobox.pack(side=LEFT)
        self.color_combobox.current(0)

        entry_container = Frame(self.root)
        entry_container.pack(side=TOP, pady=5)

        entry_x_container = Frame(entry_container)
        entry_x_container.pack(side=TOP)

        entry_y_container = Frame(entry_container)
        entry_y_container.pack(side=TOP)

        entry_z_container = Frame(entry_container)
        entry_z_container.pack(side=TOP)

        self.point_x = DoubleVar()
        self.point_y = DoubleVar()
        self.point_z = DoubleVar()
        Label(entry_x_container, text="X").pack(side=LEFT)
        Entry(entry_x_container, textvariable=self.point_x).pack(side=LEFT)
        Label(entry_y_container, text="Y").pack(side=LEFT)
        Entry(entry_y_container, textvariable=self.point_y).pack(side=LEFT)
        Label(entry_z_container, text="Z").pack(side=LEFT)
        Entry(entry_z_container, textvariable=self.point_z).pack(side=LEFT)

        buttons_container = Frame(self.root)
        buttons_container.pack(side=TOP)
        Button(buttons_container, text="Adicionar Ponto",
               command=self.add_point).pack()

        list_container = Frame(buttons_container)
        list_container.pack(side=TOP)

        self.new_object_listbox = Listbox(list_container, exportselection=0)
        self.new_object_listbox_2 = Listbox(list_container, exportselection=0)

        self.new_object_listbox.pack(pady=5, side=LEFT, padx=10)
        self.new_object_listbox_2.pack(pady=5, side=LEFT)

        Button(buttons_container, text="Adicionar Aresta",
               command=self.add_edge).pack()

        self.edges_listbox = Listbox(buttons_container, width=50)
        self.edges_listbox.pack(pady=5, side=TOP)

        self.new_object_type = IntVar()
        self.new_object_type.set(-1)

        radio_container = Frame(buttons_container)
        top_container = Frame(radio_container)
        bottom_container = Frame(radio_container)

        top_container.pack(side=TOP)
        bottom_container.pack(side=BOTTOM)
        self.radio_buttons = [Radiobutton(top_container, text="Ponto",
                                          variable=self.new_object_type, value=0),
                              Radiobutton(top_container, text="Linha",
                                          variable=self.new_object_type, value=1),
                              # Radiobutton(top_container, text="Curva (Bezier)",
                              #             variable=self.new_object_type, value=2),
                              # Radiobutton(bottom_container, text="Curva (B-Spline)",
                              #             variable=self.new_object_type, value=3),
                              Radiobutton(bottom_container, text="Forma",
                                          variable=self.new_object_type, value=4)]

        for rb in self.radio_buttons:
            rb.pack(side=LEFT)

            rb.configure(state=DISABLED)

        radio_container.pack(side=TOP)

        Button(buttons_container, text="Adicionar objeto",
               command=self.add_object_on_screen).pack()

    def add_edge(self):
        coord1 = self.new_object_listbox.curselection()[0]
        coord2 = self.new_object_listbox_2.curselection()[0]
        if (coord1 == coord2):
            return
        edge = [coord1, coord2]
        self.edges.append(edge)
        self.edges_listbox.insert(END, str(coord1) + " -> " + str(coord2))

    def add_object_on_screen(self):
        self.on_submit(self.new_object_type.get(),
                       self.object_name.get(), self.new_object_coords, self.color_combobox.get(), self.edges, True)

    def add_point(self):
        x = self.point_x.get()
        y = self.point_y.get()
        z = self.point_z.get()
        self.new_object_coords.append(Coord(x, y, z))
        self.new_object_listbox.insert(
            END, "(" + str(x) + ", " + str(y) + ", " + str(z) + ")")
        self.new_object_listbox_2.insert(
            END, "(" + str(x) + ", " + str(y) + ", " + str(z) + ")")
        self.point_x.set(0)
        self.point_y.set(0)
        self.point_z.set(0)

        self.configureRadioButtons()

    def configureRadioButtons(self):
        self.new_object_type.set(-1)
        for rb in self.radio_buttons:
            rb.configure(state=DISABLED)
        length = len(self.new_object_coords)
        if (length == 1):
            self.radio_buttons[0].configure(state=ACTIVE)
        elif (length == 2):
            self.radio_buttons[1].configure(state=ACTIVE)
        elif (length == 3):
            self.radio_buttons[1].configure(state=ACTIVE)
            self.radio_buttons[4].configure(state=ACTIVE)
        elif (length >= 4):
            self.radio_buttons[1].configure(state=ACTIVE)
            self.radio_buttons[3].configure(state=ACTIVE)
            self.radio_buttons[4].configure(state=ACTIVE)
            aux = length - 4
            if (aux % 3 == 0):
                self.radio_buttons[2].configure(state=ACTIVE)

    def destroy(self):
        self.root.destroy()
