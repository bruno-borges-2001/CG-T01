from tkinter import *


class Popup:

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

        print(self.option, self.rotation_type.get())

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
