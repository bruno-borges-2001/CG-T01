class GraphicObject:

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords
        self.centerX = 0
        self.centerY = 0
        self.getCenter()

    def translate(self, x, y):
        for i in range(len(self.coords)):
            if i % 2 == 0:
                self.coords[i] += x
            else:
                self.coords[i] += y

    def getCenter(self):
        for i in range(len(self.coords)):  # ARRAY POS PAR = X / ARRAY POS IMPAR = Y
            coord = self.coords[i]
            if (i % 2 == 0):
                self.centerX += coord
            else:
                self.centerY += coord

        self.centerX = self.centerX / (len(self.coords) / 2)
        self.centerY = self.centerY / (len(self.coords) / 2)
