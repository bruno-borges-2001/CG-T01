from tkinter import *
from classes import Wireframe


class App:
    def __init__(self):

        self.root = Tk()
        self.root.title("Interface grafica para insercao de objetos")

        self.objects = []
        self.points = []
        self.pointReaders = []

        self.leftTransform = 0
        self.rightTransform = 0
        self.topTransform = 0
        self.bottomTransform = 0
        
        self.zoomSize = 0

        self.root.geometry("1000x500")
        self.root.state('normal')

        self.render()

        self.root.update_idletasks()
        self.canvas_container.update_idletasks()
        self.canvas.update_idletasks()

    def render(self):
        self.function_container = Frame(self.root, background="red", width=30)
        self.function_container.pack(side=LEFT, fill=Y)
        
        self.header = Label(self.function_container, text="Funcoes", width=30)
        self.header.pack(side=TOP)

        self.listbox = Listbox(self.function_container, width=35)
        self.listbox.pack(side=TOP)
        
        self.add_and_remove_container = Frame(self.function_container, background="red")
        self.add_and_remove_container.pack(side=TOP, pady=20)
        
        self.up_container = Frame(self.function_container, background="red")
        self.up_container.pack(side=TOP)
        
        self.directions_container = Frame(self.function_container, background="red")
        self.directions_container.pack(side=TOP)
        
        self.zoom_container = Frame(self.function_container, background="red")
        self.zoom_container.pack(side=TOP, pady=20)

        self.canvas_container = Frame(self.root, background="green")
        self.canvas_container.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self.canvas_container, background="white")
        self.canvas.pack(fill=BOTH, expand=True)





        self.addButton = Button(self.add_and_remove_container,
                                text="Adicionar Objeto", command=self.addObject)
        self.addButton.pack()


        self.removeButton = Button(self.add_and_remove_container,
                                   text="Remover Objeto", command=self.removeObject)
        self.removeButton.pack()


        self.upButton = Button(self.up_container,
                               text="↑", command=lambda: self.transform('u'))
        self.upButton.pack(side=TOP)

        
        self.leftButton = Button(self.directions_container,
                                 text="←", command=lambda: self.transform('l'))
        self.leftButton.pack(side=LEFT)
        
        
        self.downButton = Button(self.directions_container,
                                 text="↓", command=lambda: self.transform('d'))
        self.downButton.pack(side=LEFT)
        
        
        self.rightButton = Button(self.directions_container,
                                  text="→", command=lambda: self.transform('r'))
        self.rightButton.pack(side=LEFT)


        self.zoomPlusButton = Button(self.zoom_container,
                                     text="+", command=lambda: self.zoom(1))
        self.zoomPlusButton.pack()

        
        self.zoomMinusButton = Button(self.zoom_container,
                                      text="-", command=lambda: self.zoom(-1))
        self.zoomMinusButton.pack()

    def draw(self):
        self.canvas.delete("all")
        for i in self.objects:
            tranformedCoords = self.tranformCoords(
                i.coords + i.coords[:2])
            print("Transform",self.leftTransform, self.rightTransform,
                  self.topTransform, self.bottomTransform,)

            self.canvas.create_line(tranformedCoords, tags=i.name)

    def transform(self, direction):
        if (direction == 'u'):
            self.topTransform += self.canvas.winfo_height() * 0.1
            self.bottomTransform += self.canvas.winfo_height() * 0.1
        elif (direction == 'd'):
            self.topTransform -= self.canvas.winfo_height() * 0.1
            self.bottomTransform -= self.canvas.winfo_height() * 0.1
        elif (direction == 'l'):
            self.leftTransform -= self.canvas.winfo_width() * 0.1
            self.rightTransform -= self.canvas.winfo_width() * 0.1
        elif (direction == 'r'):
            self.leftTransform += self.canvas.winfo_width() * 0.1
            self.rightTransform += self.canvas.winfo_width() * 0.1
        self.draw()

    def zoom(self, signal):
        # AINDA PRECISA MELHORAR
        self.topTransform -= signal * self.canvas.winfo_height() * 0.1
        self.bottomTransform += signal * self.canvas.winfo_height() * 0.1
        self.leftTransform -= signal * self.canvas.winfo_width() * 0.1
        self.rightTransform += signal * self.canvas.winfo_width() * 0.1
        self.draw()

    def getViewportX(self, xw, xwmin, xwmax, xvpmin, xvpmax):
        print(xwmin, xwmax, xvpmin, xvpmax)
        return (xw - xwmin) * (xwmax - xwmin) / (xvpmax - xvpmin)

    def getViewportY(self, yw, ywmin, ywmax, yvpmin, yvpmax):
        print(ywmin, ywmax, yvpmin, yvpmax)
        return (1 - ((yw - ywmin) / (ywmax - ywmin))) * (yvpmax - yvpmin)

    def tranformCoords(self, coords):
        aux = []
        XVMIN = 0
        YVMIN = 0
        XVMAX = self.canvas_container.winfo_width()
        YVMAX = self.canvas_container.winfo_height()

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

        # ESSE METODO INSTANCIA WIREFRAME COM NOME E COORDENADAS
        # ADICIONA O NOME NA LISTBOX - TALVEZ TESTAR SE NOME JA EXISTE
        # ADICIONA O OBJETO NO VETOR DE OBJETOS
        # LIMPA A TELA E DESENHA TODOS OS VETORES DO OBJETO

        
        self.add_object_screen = Toplevel(self.root)
        self.add_object_screen.title("Adicionar objeto")
        self.add_object_screen.geometry("300x600")
        
        self.nameObjectContainer = Frame(self.add_object_screen)
        self.nameObjectContainer.pack(side=TOP)
        
        self.objectName = StringVar()
        Label(self.nameObjectContainer, text="Nome do objeto:").pack(side=LEFT)
        Entry(self.nameObjectContainer, textvariable=self.objectName).pack(side=LEFT)
        
        self.buttonsContainer = Frame(self.add_object_screen)
        self.buttonsContainer.pack(side=BOTTOM)
        
        self.pointNumber = 0
        self.addPoints()
        
        Button(self.buttonsContainer, text="Adicionar pontos", command=self.addPoints).pack()
        Button(self.buttonsContainer, text="Adicionar objeto", command=self.addObjectOnScreen).pack()


    def removeObject(self):
        self.canvas.delete(self.listbox.get(self.listbox.curselection()))
        self.listbox.delete(self.listbox.curselection())
        print(self.objects)
        self.objects.pop(self.listbox.curselection()[0])
        print(self.objects)

    def startApp(self):
        self.root.mainloop()


    def addPoints(self):
        self.pointNumber += 1
        xName = "X" + str(self.pointNumber) + ":"
        yName = "Y" + str(self.pointNumber) + ":"
        entryContainer = Frame(self.add_object_screen)
        entryContainer.pack(side=TOP, pady=5)
        
        entryXContainer = Frame(entryContainer)
        entryXContainer.pack(side=TOP)
        
        entryYContainer = Frame(entryContainer)
        entryYContainer.pack(side=TOP)
        
        x = IntVar()
        y = IntVar()
        self.pointReaders.append((x,y))
        Label(entryXContainer, text=xName).pack(side=LEFT)
        Entry(entryXContainer, textvariable=x).pack(side=LEFT)
        Label(entryYContainer, text=yName).pack(side=LEFT)
        Entry(entryYContainer, textvariable=y).pack(side=LEFT)
        
        
    def addObjectOnScreen(self):
        for point in self.pointReaders:
            intX = point[0].get()
            intY = point[1].get()
            self.points.append(intX)
            self.points.append(intY)
        
        print(self.points)
        newObject = Wireframe(self.objectName.get(), self.points)
        self.pointNumber = 0
        self.points = []
        self.pointReaders = []
        self.listbox.insert(END, newObject.name)
        self.objects.append(newObject)
        self.draw()
        self.add_object_screen.destroy()
        
            
