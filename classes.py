from math import *


class GraphicObject:

    def __init__(self, name, coords, color):
        self.name = name
        self.coords = coords
        self.color = color

        self.center_x = 0
        self.center_y = 0
        self.get_center()

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

    def center_scale(self, Sx, Sy):
        self.get_center()
        for i in range(len(self.coords)):
            if i % 2 == 0:
                self.coords[i] = self.coords[i] * Sx - self.center_x * (Sx - 1)
            else:
                self.coords[i] = self.coords[i] * Sy - self.center_y * (Sy - 1)

        # self.translate(-self.centerX, -self.centerY)
        # self.scale(Sx, Sy)
        # self.translate(self.centerX, self.centerY)

    def rotate(self, Dx, Dy, teta):
        # ROTATE
        angle = (360 - teta) * (pi/180)
        coseno = round(cos(angle), 5)
        seno = round(sin(angle), 5)
        aux = [0] * len(self.coords)
        for i in range(len(self.coords)):
            if i % 2 == 0:
                x = self.coords[i]
                y = self.coords[i+1]
                aux[i] = (x - Dx) * coseno + (y - Dy) * seno + Dx
            else:
                x = self.coords[i-1]
                y = self.coords[i]
                aux[i] = (- x + Dx) * seno + (y - Dy) * coseno + Dy
        self.coords = aux

    def get_center(self):
        center_x = 0
        center_y = 0

        for i in range(len(self.coords)):  # ARRAY POS PAR = X / ARRAY POS IMPAR = Y
            coord = self.coords[i]
            if (i % 2 == 0):
                center_x += coord
            else:
                center_y += coord

        self.center_x = center_x / (len(self.coords) / 2)
        self.center_y = center_y / (len(self.coords) / 2)

    def return_center(self):
        self.get_center()
        return (self.center_x, self.center_y)
