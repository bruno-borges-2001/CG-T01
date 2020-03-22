from tkinter import *
from tkinter import ttk
from classes import GraphicObject

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

        self.leftTransform = 0
        self.rightTransform = 0
        self.topTransform = 0
        self.bottomTransform = 0

        self.zoomHeight = 0
        self.zoomWidth = 0

        # RENDER / UPDATE
        self.render()
        self.root.update_idletasks()
        self.canvas_container.update_idletasks()
        self.canvas.update_idletasks()

    def getCanvasCenter(self):
        return (self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2)

    def render(self):
        function_container = Frame(self.root, width=30)
        function_container.pack(side=LEFT, fill=Y)

        Label(function_container, text="Funcoes", width=30).pack(side=TOP)

        self.listbox = Listbox(function_container, width=35)
        self.listbox.pack(side=TOP)

        Button(function_container, width=29, text="Limpar", command=lambda: self.listbox.select_clear(0)
               ).pack(side=TOP)

        add_and_remove_container = Frame(function_container)
        add_and_remove_container.pack(side=TOP, pady=10)

        Label(function_container,
              text="Window / Objeto (selecione na listbox)", width=30).pack(side=TOP)

        mainButtonContainer = Frame(function_container, width=35)
        mainButtonContainer.pack(side=TOP)

        arrowsContainer = Frame(mainButtonContainer, padx=10)
        arrowsContainer.pack(side=LEFT)

        up_container = Frame(arrowsContainer)
        up_container.pack(side=TOP)

        directions_container = Frame(arrowsContainer)
        directions_container.pack(side=TOP)

        zoom_container = Frame(mainButtonContainer)
        zoom_container.pack(side=RIGHT, pady=10, padx=10)

        self.canvas_container = Frame(self.root)
        self.canvas_container.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self.canvas_container, background="white")
        self.canvas.pack(fill=BOTH, expand=True)

        Button(add_and_remove_container,
               text="Adicionar Objeto", command=self.addObject).pack(side=LEFT)

        Button(add_and_remove_container,
               text="Remover Objeto", command=self.removeObject).pack(side=RIGHT)

        Button(up_container,
               text="↑", command=lambda: self.handleTranslation('up')).pack(side=TOP)

        Button(directions_container,
               text="←", command=lambda: self.handleTranslation('left')).pack(side=LEFT)

        Button(directions_container,
               text="↓", command=lambda: self.handleTranslation('down')).pack(side=LEFT)

        Button(directions_container,
               text="→", command=lambda: self.handleTranslation('right')).pack(side=LEFT)

        Button(zoom_container,
               text="+", command=lambda: self.zoom(1)).pack()

        Button(zoom_container,
               text="-", command=lambda: self.zoom(-1)).pack()

        self.log = Listbox(function_container, width=35)
        self.log.pack(fill=Y, side=BOTTOM)

    def draw(self):
        self.canvas.delete("all")
        for i in self.objects:
            tranformedCoords = self.tranformCoords(
                (i.coords + i.coords[:2]) if (len(i.coords) > 4) else i.coords)
            if (len(i.coords) >= 4):
                self.canvas.create_line(
                    tranformedCoords, tags=i.name, fill=i.color)
            else:
                self.canvas.create_oval(
                    tranformedCoords[0] - 1, tranformedCoords[1] - 1, tranformedCoords[0] + 1, tranformedCoords[1] + 1, fill=i.color)

    def handleTranslation(self, direction):
        selected = self.listbox.curselection()
        if len(selected) > 0:
            values = self.getTranslateValues(direction)
            for item in selected:
                self.log.insert(
                    0, "Object " + self.objects[item].name + " moved " + direction)
                self.objects[item].translate(*values)
            self.draw()
        else:
            self.moveWindow(direction)

    def getTranslateValues(self, direction):
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

    def moveWindow(self, direction):
        if (direction == 'up'):
            self.topTransform += self.canvas.winfo_height() * 0.1
            self.bottomTransform += self.canvas.winfo_height() * 0.1
        elif (direction == 'down'):
            self.topTransform -= self.canvas.winfo_height() * 0.1
            self.bottomTransform -= self.canvas.winfo_height() * 0.1
        elif (direction == 'left'):
            self.leftTransform -= self.canvas.winfo_width() * 0.1
            self.rightTransform -= self.canvas.winfo_width() * 0.1
        elif (direction == 'right'):
            self.leftTransform += self.canvas.winfo_width() * 0.1
            self.rightTransform += self.canvas.winfo_width() * 0.1
        self.log.insert(0, "Window moved " + direction)
        self.draw()

    def zoom(self, signal):
        # self.topTransform += signal * self.canvas.winfo_height() * 0.1
        # self.bottomTransform -= signal * self.canvas.winfo_height() * 0.1
        # self.leftTransform += signal * self.canvas.winfo_width() * 0.1
        # self.rightTransform -= signal * self.canvas.winfo_width() * 0.1

        self.zoomHeight += signal * self.canvas_container.winfo_height() * 0.05
        self.zoomWidth += signal * self.canvas_container.winfo_width() * 0.05
        self.log.insert(0, "zoomed in" if signal > 0 else "zoomed out")
        self.draw()

    def getViewportX(self, xw, xwmin, xwmax, xvpmin, xvpmax):
        print(xwmin, xwmax, xvpmin, xvpmax)
        return (xw - xwmin) * (xvpmax - xvpmin) / (xwmax - xwmin)

    def getViewportY(self, yw, ywmin, ywmax, yvpmin, yvpmax):
        print(ywmin, ywmax, yvpmin, yvpmax)
        return (1 - ((yw - ywmin) / (ywmax - ywmin))) * (yvpmax - yvpmin)

    def tranformCoords(self, coords):
        aux = []
        XVMIN = 0 - self.zoomWidth
        YVMIN = 0 - self.zoomHeight
        XVMAX = self.canvas_container.winfo_width() + self.zoomWidth
        YVMAX = self.canvas_container.winfo_height() + self.zoomHeight

        XWMIN = 0 + self.leftTransform
        YWMIN = 0 + self.topTransform
        XWMAX = self.canvas_container.winfo_width() + self.rightTransform
        YWMAX = self.canvas_container.winfo_height() + self.bottomTransform

        for i in range(len(coords)):  # ARRAY POS PAR = X / ARRAY POS IMPAR = Y
            coord = coords[i]
            if (i % 2 == 0):
                aux.append(self.getViewportX(
                    coord, XWMIN, XWMAX, XVMIN, XVMAX))
            else:
                aux.append(self.getViewportY(
                    coord, YWMIN, YWMAX, YVMIN, YVMAX))
        return aux

    def addObject(self):
        # EX DE COORDENADAS => [X1, Y1, X2, Y2, X3, Y3, ..., Xn, Yn]
        self.newObjectCoords = []

        self.add_object_screen = Toplevel(self.root)
        self.add_object_screen.title("Adicionar objeto")
        self.add_object_screen.geometry("300x400")

        self.nameObjectContainer = Frame(self.add_object_screen)
        self.nameObjectContainer.pack(side=TOP)

        self.objectName = StringVar()
        Label(self.nameObjectContainer, text="Nome do objeto:").pack(side=LEFT)
        Entry(self.nameObjectContainer,
              textvariable=self.objectName).pack(side=LEFT)

        self.colorObjectContainer = Frame(
            self.add_object_screen)
        self.colorObjectContainer.pack(side=TOP)

        Label(self.colorObjectContainer, text="Cor do objeto:").pack(side=LEFT)

        self.colorCombobox = ttk.Combobox(
            self.colorObjectContainer, values=list(COLORS.keys()))
        self.colorCombobox.pack(side=LEFT)
        self.colorCombobox.current(0)

        entryContainer = Frame(self.add_object_screen)
        entryContainer.pack(side=TOP, pady=5)

        entryXContainer = Frame(entryContainer)
        entryXContainer.pack(side=TOP)

        entryYContainer = Frame(entryContainer)
        entryYContainer.pack(side=TOP)
        self.buttonsContainer = Frame(self.add_object_screen)
        self.newObjectListbox = Listbox(self.buttonsContainer)

        self.pointX = IntVar()
        self.pointY = IntVar()
        Label(entryXContainer, text="X").pack(side=LEFT)
        Entry(entryXContainer, textvariable=self.pointX).pack(side=LEFT)
        Label(entryYContainer, text="Y").pack(side=LEFT)
        Entry(entryYContainer, textvariable=self.pointY).pack(side=LEFT)

        self.buttonsContainer.pack(side=TOP)

        Button(self.buttonsContainer, text="Adicionar ponto",
               command=self.addPoint).pack()
        self.newObjectListbox.pack(pady=5)
        Button(self.buttonsContainer, text="Adicionar objeto",
               command=self.addObjectOnScreen).pack()

    def removeObject(self):
        self.log.insert(
            0, "Object " + self.listbox.get(self.listbox.curselection()) + " removed")
        self.canvas.delete(self.listbox.get(self.listbox.curselection()))
        self.objects.pop(self.listbox.curselection()[0])
        self.listbox.delete(self.listbox.curselection())

    def startApp(self):
        self.root.mainloop()

    def addPoint(self):
        x = self.pointX.get()
        y = self.pointY.get()
        self.newObjectCoords += [x, y]
        print(self.newObjectCoords)
        self.newObjectListbox.insert(END, "(" + str(x) + "," + str(y) + ")")
        self.pointX.set(0)
        self.pointY.set(0)

    def addObjectOnScreen(self):
        if (len(self.objectName.get()) > 0 and len(self.newObjectCoords) > 0):
            print(self.newObjectCoords)
            newObject = GraphicObject(
                self.objectName.get(), self.newObjectCoords, COLORS[self.colorCombobox.get()])
            self.listbox.insert(END, newObject.name)
            self.log.insert(0, "Objected " + newObject.name + " added")
            self.objects.append(newObject)
            self.draw()
            self.add_object_screen.destroy()

    def translateObject(self, translateX, translateY):
        object = self.objects[self.listbox.curselection()[0]]
        for i in range(len(object.coords)):  # ARRAY POS PAR = X / ARRAY POS IMPAR = Y
            if (i % 2 == 0):
                object.coords[i] += translateX
            else:
                object.coords[i] += translateY
