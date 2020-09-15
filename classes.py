from math import *


class Coords:

    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        if not z:
            self.z = 1
        else:
            self.z = z

    def to_list(self):
        return [self.x, self.y, self.z]

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"


class Matrix:

    def __init__(self, height, width, values=None):
        self.height = height
        self.width = width
        if not values:
            self.createEmptyMatrix()
        else:
            self.matrix = values

    def createEmptyMatrix(self):
        self.matrix = [[0 for j in range(self.width)]
                       for i in range(self.height)]

    def __add__(self, other):
        if (self.height != other.height or self.width != other.width):
            return False
        result = Matrix(self.height, self.width)
        for i in range(self.height):
            for j in range(self.width):
                result.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return result

    def __mul__(self, other):
        if (self.width != other.height):
            return False
        result = Matrix(self.height, other.width)
        for i in range(self.height):
            for j in range(other.width):
                for k in range(other.height):
                    result.matrix[i][j] += self.matrix[i][k] * \
                        other.matrix[k][j]
        return result


class CalculationMatrix(Matrix):

    def __init__(self, module, values):
        if module == 'c':
            super().__init__(1, 3, [values])
        elif module == 't':
            super().__init__(
                3, 3, [[1, 0, 0], [0, 1, 0], [values[0], values[1], 0]])
        elif module == 's':
            super().__init__(
                3, 3, [[values[0], 0, 0], [0, values[1], 0], [0, 0, 1]])
        elif module == 'r':
            angle = (360 - values) * (pi/180)
            coseno = round(cos(angle), 5)
            seno = round(sin(angle), 5)
            super().__init__(
                3, 3, [[coseno, -seno, 0], [seno, coseno, 0], [0, 0, 1]])

class GraphicObject:

    def __init__(self, name, coords, color):
        self.name = name
        self.coords = coords
        self.color = color
        self.get_center()

    def center_scale(self, Sx, Sy):
        self.get_center()

        self.translate(-self.center.x, -self.center.y)
        self.scale(Sx, Sy)
        self.translate(self.center.x, self.center.y)

    def get_center(self):
        center_x = 0
        center_y = 0

        for coord in self.coords:  # ARRAY POS PAR = X / ARRAY POS IMPAR = Y
            center_x += coord.x
            center_y += coord.y

        self.center = Coords(center_x / (len(self.coords)),
                             center_y / (len(self.coords)))

    def scale(self, Sx, Sy):
        aux = []
        for coord in self.coords:
            result = CalculationMatrix('c', coord.to_list()) * \
                CalculationMatrix('s', [Sx, Sy])
            aux.append(Coords(*result.matrix[0]))
        self.coords = aux

    def return_center(self):
        self.get_center()
        return self.center

    def rotate(self, Dx, Dy, teta):
        self.translate(-Dx, -Dy)

        aux = []
        for coord in self.coords:
            result = CalculationMatrix('c', coord.to_list()) * \
                CalculationMatrix('r', teta)
            aux.append(Coords(*result.matrix[0]))
        self.coords = aux

        self.translate(Dx, Dy)

    def translate(self, Cx, Cy):
        aux = []
        for coord in self.coords:
            result = CalculationMatrix('c', coord.to_list()) * \
                CalculationMatrix('t', [Cx, Cy])
            aux.append(Coords(*result.matrix[0]))
        self.coords = aux
