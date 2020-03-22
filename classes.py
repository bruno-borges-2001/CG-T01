class GraphicObject:

    def __init__(self, name, coords, color):
        self.name = name
        self.coords = coords
        self.color = color

        self.centerX = 0
        self.centerY = 0
        self.getCenter()

    def translate(self, Cx, Cy):
        for i in range(len(self.coords)):
            if i % 2 == 0:
                self.coords[i] += Cx
            else:
                self.coords[i] += Cy

    def scale(self, Sx, Sy):
        for i in range(len(self.coords)):
            if i % 2 == 0:
                self.coords[i] *= Sx
            else:
                self.coords[i] *= Sy

    def centerScale(self, Sx, Sy):
        self.translate(-self.centerX, -self.centerY)
        self.scale(Sx, Sy)
        self.translate(self.centerX, self.centerY)

    def getCenter(self):
        for i in range(len(self.coords)):  # ARRAY POS PAR = X / ARRAY POS IMPAR = Y
            coord = self.coords[i]
            if (i % 2 == 0):
                self.centerX += coord
            else:
                self.centerY += coord

        self.centerX = self.centerX / (len(self.coords) / 2)
        self.centerY = self.centerY / (len(self.coords) / 2)
