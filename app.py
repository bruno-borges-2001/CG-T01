from tkinter import *
from classes import Wireframe


class App:
    def __init__(self):

        self.root = Tk()
        self.root.title = "teste"

        self.root.geometry("1000x500")
        self.root.state('zoomed')

        self.render()

        self.root.update_idletasks()
        self.canvas_container.update_idletasks()

    def render(self):
        self.function_container = Frame(self.root, background="red", width=30)
        self.function_container.pack(side=LEFT, fill=Y)

        self.canvas_container = Frame(self.root, background="green")
        self.canvas_container.pack(fill=Y, expand=True)

        self.canvas = Canvas(self.canvas_container, background="white")
        self.canvas.pack(fill=BOTH, expand=True)

        self.header = Label(self.function_container, text="Funções", width=30)
        self.header.pack()

        self.listbox = Listbox(self.function_container, width=35)
        self.listbox.pack()

        self.addButton = Button(self.function_container,
                                text="Adicionar Objeto", command=self.addObject)
        self.addButton.pack()

        self.removeButton = Button(self.function_container,
                                   text="Remover Objeto", command=self.removeObject)
        self.removeButton.pack()

    def getViewportX(self, xw, xwmin, xwmax, xvpmin, xvpmax):
        return (xw - xwmin) * (xwmax - xwmin) / (xvpmax - xvpmin)

    def getViewportY(self, yw, ywmin, ywmax, yvpmin, yvpmax):
        return (1 - ((yw - ywmin) / (ywmax - ywmin))) * (yvpmax - yvpmin)

    def tranformCoords(self, coords):
        aux = coords
        for i in range(len(coords)):
            coord = coords[i]
            window_min = 0
            window_max = self.canvas_container.winfo_width()
            if (i % 2 == 0):
                aux[i] = self.getViewportX(
                    coord, window_min, window_max, window_min, window_max)
            else:
                aux[i] = self.getViewportY(
                    coord, window_min, window_max, window_min, window_max)
        return aux

    def addObject(self):
        newObject = Wireframe("test", [100, 20, 40, 50, 30, 10])
        self.listbox.insert(END, newObject.name)
        tranformedCoords = self.tranformCoords(
            newObject.coords + newObject.coords[:2])
        self.canvas.create_line(tranformedCoords, tags=newObject.name)

    def removeObject(self):
        self.canvas.delete(self.listbox.get(self.listbox.curselection()))
        self.listbox.delete(self.listbox.curselection())

    def startApp(self):
        self.root.mainloop()
