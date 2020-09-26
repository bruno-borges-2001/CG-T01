from math import *
from copy import deepcopy
# import numpy


class Coord:

    def __init__(self, x, y, z=None, artificial=False):
        self.x = x
        self.y = y
        if not z:
            self.z = 1
        else:
            self.z = z

        self.artificial = artificial

    def to_list(self):
        return [self.x, self.y, self.z]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return "(" + str(round(self.x, 2)) + "," + str(round(self.y, 2)) + ")"


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
        elif module == 'Mb':
            super().__init__(
                4, 4, [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
        elif module == 'T':
            super().__init__(
                1, 4, [[pow(values, 3), pow(values, 2), values, 1]])
        elif module == 'G':
            super().__init__(
                4, 1, [[values[0]], [values[1]], [values[2]], [values[3]]])


class GraphicObject:

    def __init__(self, name, coords, color, normalized=False, typeF=None, ready=False):
        self.name = name
        self.coords = coords
        self.color = color

        self.normalized = normalized

        self.clipped = []

        if (len(coords) == 1):
            self.type = "point"
            self.clip_point()
        elif (len(coords) == 2):
            self.type = "line"
            self.clip_line()
        elif (len(coords) > 2):
            self.type = typeF
            if (typeF == "curve"):
                if (not ready):
                    self.bezier()
                self.clip_curve()
            else:
                self.clip_polygon()

        self.get_center()

    def bezier(self):
        curve_coords = []
        mb = CalculationMatrix('Mb', [])
        for i in range(floor(len(self.coords)/3)):
            p1 = self.coords[3*i]
            p2 = self.coords[3*i + 1]
            p3 = self.coords[3*i + 2]
            p4 = self.coords[3*i + 3]
            gbx = CalculationMatrix('G', [p1.x, p2.x, p3.x, p4.x])
            gby = CalculationMatrix('G', [p1.y, p2.y, p3.y, p4.y])
            # numpy.arange(0, 1.005, 0.005)
            for t in range(0, 1005, 5):
                aux = t/1000
                matrix_t = CalculationMatrix('T', aux)
                ptx = matrix_t * mb * gbx
                pty = matrix_t * mb * gby
                coord = Coord(ptx.matrix[0][0], pty.matrix[0][0])
                curve_coords.append(coord)
        self.coords = curve_coords

    def calculate_intersection(self, p1, p2, prc):
        intersects = True
        rc_intersects = False
        new_coords = deepcopy([p1, p2])
        for i in range(2):
            if (intersects):
                rc = prc[i]
                if (rc & int('0001', 2) == int('0001', 2)):  # left intersection
                    m = (p2.y - p1.y) / (p2.x - p1.x)
                    y = m * (-1 - p1.x) + p1.y
                    if (y >= -1 and y <= 1):
                        rc_intersects = True
                        new_coords[i].x = -1
                        new_coords[i].y = y
                    else:
                        intersects = rc_intersects
                if (rc & int('0010', 2) == int('0010', 2)):  # right intersection
                    m = (p2.y - p1.y) / (p2.x - p1.x)
                    y = m * (1 - p1.x) + p1.y
                    if (y >= -1 and y <= 1):
                        rc_intersects = True
                        new_coords[i].x = 1
                        new_coords[i].y = y
                    else:
                        intersects = rc_intersects
                if (rc & int('0100', 2) == int('0100', 2)):  # bottom intersection
                    m = (p2.x - p1.x) / (p2.y - p1.y)
                    x = p1.x + m * (-1 - p1.y)
                    if (x >= -1 and x <= 1):
                        rc_intersects = True
                        new_coords[i].x = x
                        new_coords[i].y = -1
                    else:
                        intersects = rc_intersects
                if (rc & int('1000', 2) == int('1000', 2)):  # top intersection
                    m = (p2.x - p1.x) / (p2.y - p1.y)
                    x = p1.x + m * (1 - p1.y)
                    if (x >= -1 and x <= 1):
                        rc_intersects = True
                        new_coords[i].x = x
                        new_coords[i].y = 1
                    else:
                        intersects = rc_intersects
        intersects = rc_intersects
        return (intersects, new_coords)

    def clip_point(self):
        if (not self.normalized):
            pass
        self.clipped = []
        if (self.inside(self.coords[0])):
            self.clipped.append(self.coords)

    def clip_line(self, coords=False, return_value=False):
        if (not self.normalized):
            pass
        if (not coords):
            self.clipped = []
            coords = self.coords
        # checking position of points
        prc = self.set_region_codes(coords)
        if (prc[0] == 0 and prc[1] == 0):
            if (return_value):
                return coords
            else:
                self.clipped.append(coords)
        elif (prc[0] & prc[1] != 0):
            if (return_value):
                return []
            else:
                pass
        elif (prc[0] & prc[1] == 0 and prc[0] != prc[1]):
            [intersects, new_coords] = self.calculate_intersection(
                coords[0], coords[1], prc)
            if (return_value):
                return new_coords if intersects else []
            else:
                if (intersects):
                    self.clipped.append(new_coords)

    def clip_curve(self):
        i = 0
        while i < len(self.coords) - 1:
            p1 = deepcopy(self.coords[i])
            p2 = deepcopy(self.coords[i+1])
            self.clip_line([p1, p2])
            i += 1

    def clip_polygon(self):
        if (not self.normalized):
            return
        self.clipped = []
        i = 0
        polygon = deepcopy(self.coords)
        window = []
        entrantes = []
        temp = []
        top = [Coord(-1, 1)]
        right = [Coord(1, 1)]
        bottom = [Coord(1, -1)]
        left = [Coord(-1, -1)]
        while i < len(polygon):
            p1 = deepcopy(polygon[i])
            p2 = deepcopy(polygon[(i+1) % len(polygon)])
            new_coords = self.clip_line([p1, p2], True)

            for coord in new_coords:
                coord.artificial = True
                entered = False
                if (new_coords.index(coord) == 0 and not self.inside(p1) and coord not in entrantes):
                    entrantes.append(coord)
                    entered = True
                # polygon insert
                if (coord not in polygon):
                    polygon.insert(i+1, coord)
                    i += 1
                elif (entered):
                    polygon[i+1].artificial = True
                #   window insert
                inserted = False
                if (coord.y == 1):
                    for j in range(1, len(top)):
                        if (coord.x == top[j].x):
                            inserted = True
                            break
                        if (coord.x < top[j].x):
                            top.insert(j, coord)
                            inserted = True
                            break
                    if (not inserted and abs(coord.x) != 1):
                        top.append(coord)
                if (coord.x == 1):
                    for j in range(1, len(right)):
                        if (coord.y == right[j].y):
                            inserted = True
                            break
                        if (coord.y > right[j].y):
                            right.insert(j, coord)
                            inserted = True
                            break
                    if (not inserted and abs(coord.y) != 1):
                        right.append(coord)
                if (coord.y == -1):
                    for j in range(1, len(bottom)):
                        if (coord.x == bottom[j].x):
                            inserted = True
                            break
                        if (coord.x > bottom[j].x):
                            bottom.insert(j, coord)
                            inserted = True
                            break
                    if (not inserted and abs(coord.x) != 1):
                        bottom.append(coord)
                if (coord.x == -1):
                    for j in range(1, len(left)):
                        if (coord.y == left[j].y):
                            inserted = True
                            break
                        if (coord.y < left[j].y):
                            left.insert(j, coord)
                            inserted = True
                            break
                    if (not inserted and abs(coord.y) != 1):
                        left.append(coord)
            i += 1
        window = top + right + bottom + left

        if (len(entrantes) > 0):
            temp.append([])
            for e in entrantes:
                if (e in polygon):
                    i = (polygon.index(e) + 1) % len(polygon)
                    temp[-1].append(e)
                    if (polygon[i-1].artificial):
                        while not polygon[i].artificial:
                            if (self.inside(polygon[i])):
                                temp[-1].append(polygon[i])
                            i = (i+1) % len(polygon)
                if (e not in polygon or polygon[i] != e):
                    aux = e if e not in polygon else polygon[i]
                    temp[-1].append(aux)
                    i = (window.index(aux)+1) % len(window)
                    while not window[i].artificial:
                        temp[-1].append(window[i])
                        i = (i+1) % len(window)
                    temp[-1].append(window[i])
                    if (window[i] == e):
                        temp.append([])
            self.clipped = temp
        else:
            self.clipped = [list(filter(lambda el: self.inside(el), polygon))]

    def center_scale(self, Sx, Sy):
        self.get_center()

        self.translate(-self.center.x, -self.center.y)
        self.scale(Sx, Sy)
        self.translate(self.center.x, self.center.y)

    def get_center(self):
        center_x = 0
        center_y = 0

        for coord in self.coords:
            center_x += coord.x
            center_y += coord.y

        self.center = Coord(center_x / (len(self.coords)),
                            center_y / (len(self.coords)))

    def inside(self, coord):
        return abs(coord.x) <= 1 and abs(coord.y) <= 1

    def scale(self, Sx, Sy):
        aux = []
        for coord in self.coords:
            result = CalculationMatrix('c', coord.to_list()) * \
                CalculationMatrix('s', [Sx, Sy])
            aux.append(Coord(*result.matrix[0]))
        self.coords = aux

    def set_region_codes(self, coords):
        points_region_codes = []

        for coord in coords:
            region_code = int('0000', 2)
            if (coord.x < -1):
                region_code = region_code | int('0001', 2)
            if (coord.x > 1):
                region_code = region_code | int('0010', 2)
            if (coord.y < -1):
                region_code = region_code | int('0100', 2)
            if (coord.y > 1):
                region_code = region_code | int('1000', 2)
            points_region_codes.append(region_code)
        return points_region_codes

    def return_center(self):
        self.get_center()
        return self.center

    def rotate(self, Dx, Dy, teta):
        self.translate(-Dx, -Dy)

        aux = []
        for coord in self.coords:
            result = CalculationMatrix('c', coord.to_list()) * \
                CalculationMatrix('r', teta)
            aux.append(Coord(*result.matrix[0]))
        self.coords = aux

        self.translate(Dx, Dy)

    def translate(self, Cx, Cy):
        aux = []
        for coord in self.coords:
            result = CalculationMatrix('c', coord.to_list()) * \
                CalculationMatrix('t', [Cx, Cy])
            aux.append(Coord(*result.matrix[0]))
        self.coords = aux
