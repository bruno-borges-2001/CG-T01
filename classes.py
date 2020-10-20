from math import *
from copy import deepcopy


class Coord:

    def __init__(self, x, y, z=0, artificial=False):
        self.x = x
        self.y = y
        self.z = z

        self.artificial = artificial

    def to_list(self):
        return [self.x, self.y, self.z]

    def project(self):
        return Coord(self.x, self.y)

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if (type(other) is int):
            return Coord(self.x * other, self.y * other, self.z * other)
        else:
            return Coord(self.x * other.x, self.y * other.y, self.z * other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return "(" + str(round(self.x, 2)) + "," + str(round(self.y, 2)) + "," + str(round(self.z, 2)) + ")"


class Matrix:

    def __init__(self, height, width, values=None):
        self.height = height
        self.width = width
        if not values:
            self.createEmptyMatrix()
        else:
            self.matrix = values

    def translate_matrix(self):
        aux = []
        for i in range(self.width):
            aux_column = []
            for j in range(self.height):
                aux_column.append(self.matrix[j][i])
            aux.append(aux_column)
        return Matrix(self.width, self.height, aux)

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

    def __str__(self):
        string = ""
        for line in self.matrix:
            for el in line:
                string += str(el)
                string += " "
            string += "\n"
        return string


class CalculationMatrix(Matrix):

    def __init__(self, module, values):
        if module == 'c':
            super().__init__(1, 3, [values])
        elif module == 'c3d':
            super().__init__(1, 4, [[values[0], values[1], values[2], 1]])
        elif module == 't':
            super().__init__(
                3, 3, [[1, 0, 0], [0, 1, 0], [values[0], values[1], 0]])
        elif module == 't3D':
            super().__init__(
                4, 4, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [values[0], values[1], values[2], 1]])
        elif module == 's':
            super().__init__(
                3, 3, [[values[0], 0, 0], [0, values[1], 0], [0, 0, 1]])
        elif module == 's3D':
            super().__init__(
                4, 4, [[values[0], 0, 0, 0], [0, values[1], 0, 0], [0, 0, values[2], 0], [0, 0, 0, 1]])
        elif module == 'r':
            angle = (360 - values) * (pi / 180)
            coseno = round(cos(angle), 5)
            seno = round(sin(angle), 5)
            super().__init__(
                3, 3, [[coseno, -seno, 0], [seno, coseno, 0], [0, 0, 1]])
        elif module == 'rx3D':
            angle = (360 - values) * (pi / 180)
            coseno = round(cos(angle), 5)
            seno = round(sin(angle), 5)
            super().__init__(
                4, 4, [[1, 0, 0, 0], [0, coseno, seno, 0], [0, -seno, coseno, 0], [0, 0, 0, 1]])
        elif module == 'ry3D':
            angle = (360 - values) * (pi / 180)
            coseno = round(cos(angle), 5)
            seno = round(sin(angle), 5)
            super().__init__(
                4, 4, [[coseno, 0, -seno, 0], [0, 1, 0, 0], [seno, 0, coseno, 0], [0, 0, 0, 1]])
        elif module == 'rz3D':
            angle = (360 - values) * (pi / 180)
            coseno = round(cos(angle), 5)
            seno = round(sin(angle), 5)
            super().__init__(
                4, 4, [[coseno, seno, 0, 0], [-seno, coseno, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        elif module == 'Mb':
            super().__init__(
                4, 4, [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
        elif module == 'Mbs':
            super().__init__(
                4, 4, [[-1/6, 3/6, -3/6, 1/6], [3/6, -6/6, 3/6, 0], [-3/6, 0, 3/6, 0],
                       [1/6, 4/6, 1/6, 0]])
        elif module == 'T':
            super().__init__(
                1, 4, [[pow(values, 3), pow(values, 2), values, 1]])
        elif module == 'G':
            super().__init__(
                4, 1, [[values[0]], [values[1]], [values[2]], [values[3]]])
        elif module == 'G3D':
            super().__init__(
                4, 4, [[values[0], values[1], values[2], values[3]], 
                    [values[4], values[5], values[6], values[7]], 
                    [values[8], values[9], values[10], values[11]],
                    [values[12], values[13], values[14], values[15]]])
        elif module == 'delta':
            d = values
            d2 = pow(values, 2)
            d3 = pow(values, 3)
            super().__init__(
                4, 4, [[0, 0, 0, 1], [d3, d2, d, 0], [6 * d3, 2 * d2, 0, 0], [6 * d3, 0, 0, 0]])
        elif module == 'Mper':
            super().__init__(
                4, 4, [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1/values, 0]])


class GraphicObject:

    def __init__(self, name, coords, color, normalized=False, typeF=None, ready=False):
        self.name = name
        self.coords = coords
        self.color = color

        self.normalized = normalized

        self.projected = []
        self.clipped = []

        if (len(coords) == 1):
            self.type = "point"
            self.clip_point()
        elif (len(coords) == 2):
            self.type = "line"
            self.clip_line()
        elif (len(coords) > 2):
            self.type = typeF
            if (typeF == "polygon"):
                self.clip_polygon()
            else:
                if (typeF == "curve" and not ready):
                    self.bezier()
                elif (typeF == "b_spline_curve" and not ready):
                    self.b_spline()
                self.clip_curve()

        self.get_center()

    def bezier(self):
        curve_coords = []
        mb = CalculationMatrix('Mb', [])
        for i in range(floor(len(self.coords) / 3)):
            p1 = self.coords[3 * i]
            p2 = self.coords[3 * i + 1]
            p3 = self.coords[3 * i + 2]
            p4 = self.coords[3 * i + 3]
            gbx = CalculationMatrix('G', [p1.x, p2.x, p3.x, p4.x])
            gby = CalculationMatrix('G', [p1.y, p2.y, p3.y, p4.y])
            for t in range(0, 1005, 5):
                aux = t / 1000
                matrix_t = CalculationMatrix('T', aux)
                ptx = matrix_t * mb * gbx
                pty = matrix_t * mb * gby
                coord = Coord(ptx.matrix[0][0], pty.matrix[0][0])
                curve_coords.append(coord)
        self.coords = curve_coords

    def b_spline(self):
        curve_coords = []
        mbs = CalculationMatrix('Mbs', [])
        delta = 0.01
        matrix_delta = CalculationMatrix('delta', delta)
        n = 1 / delta
        for i in range(len(self.coords) - 3):
            p1 = self.coords[i]
            p2 = self.coords[i + 1]
            p3 = self.coords[i + 2]
            p4 = self.coords[i + 3]
            gbsx = CalculationMatrix('G', [p1.x, p2.x, p3.x, p4.x])
            gbsy = CalculationMatrix('G', [p1.y, p2.y, p3.y, p4.y])

            cx = mbs * gbsx
            cy = mbs * gbsy

            fsx = matrix_delta * cx
            fsy = matrix_delta * cy

            curve_coords_aux = self.forward_difference_curve(n,
                                                             fsx.matrix[0][0], fsx.matrix[1][0], fsx.matrix[2][0],
                                                             fsx.matrix[3][0],
                                                             fsy.matrix[0][0], fsy.matrix[1][0], fsy.matrix[2][0],
                                                             fsy.matrix[3][0])
            curve_coords += curve_coords_aux
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

    def center_scale(self, Sx, Sy, _=None):
        self.get_center()

        self.translate(-self.center.x, -self.center.y)
        self.scale(Sx, Sy)
        self.translate(self.center.x, self.center.y)

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
            p2 = deepcopy(self.coords[i + 1])
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
            p2 = deepcopy(polygon[(i + 1) % len(polygon)])
            new_coords = self.clip_line([p1, p2], True)

            for coord in new_coords:
                coord.artificial = True
                entered = False
                if (new_coords.index(coord) == 0 and not self.inside(p1) and coord not in entrantes):
                    entrantes.append(coord)
                    entered = True
                # polygon insert
                if (coord not in polygon):
                    polygon.insert(i + 1, coord)
                    i += 1
                elif (entered):
                    polygon[i + 1].artificial = True
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
                    if (polygon[i - 1].artificial):
                        while not polygon[i].artificial:
                            if (self.inside(polygon[i])):
                                temp[-1].append(polygon[i])
                            i = (i + 1) % len(polygon)
                if (e not in polygon or polygon[i] != e):
                    aux = e if e not in polygon else polygon[i]
                    temp[-1].append(aux)
                    i = (window.index(aux) + 1) % len(window)
                    while not window[i].artificial:
                        temp[-1].append(window[i])
                        i = (i + 1) % len(window)
                    temp[-1].append(window[i])
                    if (window[i] == e):
                        temp.append([])
            self.clipped = temp
        else:
            self.clipped = [list(filter(lambda el: self.inside(el), polygon))]

    def forward_difference_curve(self, n, x, dx, d2x, d3x, y, dy, d2y, d3y):
        curve_coords = []
        i = 1
        curve_coords.append(Coord(x, y))
        while (i < n):
            i += 1

            x += dx
            dx += d2x
            d2x += d3x

            y += dy
            dy += d2y
            d2y += d3y

            curve_coords.append(Coord(x, y))
        return curve_coords

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

    def scale(self, Sx, Sy, _=None):
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

    def translate(self, Cx, Cy, _=None):
        aux = []
        for coord in self.coords:
            result = CalculationMatrix('c', coord.to_list()) * \
                CalculationMatrix('t', [Cx, Cy])
            aux.append(Coord(*result.matrix[0]))
        self.coords = aux


class GraphicObject3D(GraphicObject):

    def __init__(self, name, coords, edges, color, typeF=None, ready=False):
        self.coords3d = coords
        self.edges = edges
        super().__init__(name, coords, color, False, typeF if typeF else '3d', ready)

        self.angle_x = 0
        self.angle_z = 0

        self.get_center()

    def clip(self):
        for coord in self.coords:
            if (coord.z < 0):
                self.clipped = []
                return
        aux = []
        for edge in self.edges:
            p1 = self.coords[edge[0]]
            p2 = self.coords[edge[1]]
            new_values = self.clip_line([p1, p2], True)
            if (len(new_values) == 0):
                continue
            else:
                new_edge = deepcopy(edge)
                if (p1 != new_values[0]):
                    new_edge[0] = new_values[0]
                elif (p2 != new_values[1]):
                    new_edge[1] = new_values[1]
                aux.append(new_edge)
        self.clipped = aux

    def clip_polygon(self):
        if (self.normalized):
            self.clip()

    def clip_curve(self):
        if (self.normalized):
            self.clip()

    def projection(self, vrp, vpn, teta_x, teta_y, mode, cop_distance=0):
        if mode == 'parallel':
            self.translate(-vrp.x, -vrp.y, -vrp.z)
        else:
            self.translate(-vrp.x, -vrp.y, -vrp.z + cop_distance)

        rot_x = CalculationMatrix("rx3D", teta_x)
        rot_y = CalculationMatrix("ry3D", teta_y)
        aux = []
        for coord in self.coords3d:
            result = CalculationMatrix('c3d', coord.to_list()) * rot_x * rot_y
            aux.append(Coord(*result.matrix[0][:-1]))

        self.coords3d = aux

        if mode == 'perspective':
            aux_projection = []
            for coord in self.coords3d:
                w = coord.z / cop_distance
                if (w == 0):
                    aux_projection = self.coords3d
                    break
                new_coord = Coord(coord.x/w, coord.y/w, cop_distance)
                aux_projection.append(new_coord)
            self.coords = aux_projection
            self.translate(0, 0, -cop_distance)
        else:
            self.coords = list(map(lambda x: x.project(), self.coords3d))
        if self.type == "curve":
            self.edges = []
            for i in range(len(self.coords) - 1):
                self.edges.append([i, i+1])

    def center_scale(self, Sx, Sy, Sz):
        self.get_center()

        self.translate(-self.center.x, -self.center.y, -self.center.z)
        self.scale(Sx, Sy, Sz)
        self.translate(self.center.x, self.center.y, self.center.z)

    def get_center(self):
        center_x = 0
        center_y = 0
        center_z = 0

        for coord in self.coords3d:
            center_x += coord.x
            center_y += coord.y
            center_z += coord.z

        self.center = Coord(center_x / (len(self.coords3d)),
                            center_y / (len(self.coords3d)),
                            center_z / (len(self.coords3d)))

    def inside(self, coord):
        return abs(coord.x) <= 1 and abs(coord.y) <= 1

    def scale(self, Sx, Sy, Sz):
        aux = []
        for coord in self.coords3d:
            result = CalculationMatrix('c3d', coord.to_list()) * \
                CalculationMatrix('s3D', [Sx, Sy, Sz])
            aux.append(Coord(*result.matrix[0]))
        self.coords3d = aux

    def return_center(self):
        self.get_center()
        return self.center

    def rotate(self, Dx, Dy, Dz, teta):
        self.translate(-Dx, -Dy, -Dz)

        self.get_center()
        # self.angle_x = atan(self.center.y / self.center.z)
        # self.angle_z = atan(self.center.y / self.center.x)

        aux = []
        for coord in self.coords3d:
            result = CalculationMatrix('c3d', coord.to_list()) * CalculationMatrix('rx3D', self.angle_x) * \
                CalculationMatrix('rz3D', self.angle_z) * CalculationMatrix('ry3D', teta) * \
                CalculationMatrix('rz3D', 360 - self.angle_x) * \
                CalculationMatrix('rx3D', 360 - self.angle_z)
            aux.append(Coord(*result.matrix[0][:-1]))
        self.coords3d = aux

        self.translate(Dx, Dy, Dz)

    def rotate_x(self, Dx, Dy, Dz, teta):
        self.translate(-Dx, -Dy, -Dz)

        aux = []
        for coord in self.coords3d:
            result = CalculationMatrix(
                'c3d', coord.to_list()) * CalculationMatrix('rx3D', teta)
            aux.append(Coord(*result.matrix[0][:-1]))
        self.coords3d = aux

        self.translate(Dx, Dy, Dz)

    def rotate_y(self, Dx, Dy, Dz, teta):
        self.translate(-Dx, -Dy, -Dz)

        aux = []
        for coord in self.coords3d:
            result = CalculationMatrix(
                'c3d', coord.to_list()) * CalculationMatrix('ry3D', teta)
            aux.append(Coord(*result.matrix[0][:-1]))
        self.coords3d = aux

        self.translate(Dx, Dy, Dz)

    def rotate_z(self, Dx, Dy, Dz, teta):
        self.translate(-Dx, -Dy, -Dz)

        aux = []
        for coord in self.coords3d:
            result = CalculationMatrix(
                'c3d', coord.to_list()) * CalculationMatrix('rz3D', teta)
            aux.append(Coord(*result.matrix[0][:-1]))
        self.coords3d = aux

        self.translate(Dx, Dy, Dz)

    def center_rotate(self, teta, axis):
        if (axis == 'x'):
            self.rotate_x(*self.return_center().to_list(), teta)
        elif (axis == 'y'):
            self.rotate_y(*self.return_center().to_list(), teta)
        elif (axis == 'z'):
            self.rotate_z(*self.return_center().to_list(), teta)

    def translate(self, Cx, Cy, Cz):
        aux = []
        for coord in self.coords3d:
            result = CalculationMatrix('c3d', coord.to_list()) * \
                CalculationMatrix('t3D', [Cx, Cy, Cz])
            aux.append(Coord(*result.matrix[0]))
        self.coords3d = aux

    def bezier(self):
        curve_coords = []
        mb = CalculationMatrix('Mb', [])
        for i in range(1, floor(len(self.coords3d)/16) + 1):
            xs = [self.coords3d[16*i-16].x, self.coords3d[16*i-15].x, self.coords3d[16*i-14].x, self.coords3d[16*i-13].x,
                self.coords3d[16*i-12].x, self.coords3d[16*i-11].x, self.coords3d[16*i-10].x, self.coords3d[16*i-9].x,
                self.coords3d[16*i-8].x, self.coords3d[16*i-7].x, self.coords3d[16*i-6].x, self.coords3d[16*i-5].x,
                self.coords3d[16*i-4].x, self.coords3d[16*i-3].x, self.coords3d[16*i-2].x, self.coords3d[16*i-1].x]

            ys = [self.coords3d[16*i-16].y, self.coords3d[16*i-15].y, self.coords3d[16*i-14].y, self.coords3d[16*i-13].y,
                self.coords3d[16*i-12].y, self.coords3d[16*i-11].y, self.coords3d[16*i-10].y, self.coords3d[16*i-9].y,
                self.coords3d[16*i-8].y, self.coords3d[16*i-7].y, self.coords3d[16*i-6].y, self.coords3d[16*i-5].y,
                self.coords3d[16*i-4].y, self.coords3d[16*i-3].y, self.coords3d[16*i-2].y, self.coords3d[16*i-1].y]

            zs = [self.coords3d[16*i-16].z, self.coords3d[16*i-15].z, self.coords3d[16*i-14].z, self.coords3d[16*i-13].z,
                self.coords3d[16*i-12].z, self.coords3d[16*i-11].z, self.coords3d[16*i-10].z, self.coords3d[16*i-9].z,
                self.coords3d[16*i-8].z, self.coords3d[16*i-7].z, self.coords3d[16*i-6].z, self.coords3d[16*i-5].z,
                self.coords3d[16*i-4].z, self.coords3d[16*i-3].z, self.coords3d[16*i-2].z, self.coords3d[16*i-1].z]

            gbx = CalculationMatrix('G3D', xs)
            gby = CalculationMatrix('G3D', ys)
            gbz = CalculationMatrix('G3D', zs)

            x_composed = mb * gbx * mb
            y_composed = mb * gby * mb
            z_composed = mb * gbz * mb
            
            for s in range(0, 1030, 30):
                aux = s / 1000
                matrix_s = CalculationMatrix('T', aux)
                for t in range(0, 1030, 30):
                    aux = t / 1000
                    matrix_t = CalculationMatrix('T', aux).translate_matrix()
                    ptx = matrix_s * x_composed * matrix_t
                    pty = matrix_s * y_composed * matrix_t
                    ptz = matrix_s * z_composed * matrix_t
                    coord = Coord(ptx.matrix[0][0], pty.matrix[0][0], ptz.matrix[0][0])
                    curve_coords.append(coord)
        self.coords3d = curve_coords


    def b_spline(self):
        curve_coords = []
        mbs = CalculationMatrix('Mbs', [])
        
        for i in range(1, floor(len(self.coords3d)/16) + 1):
            xs = [self.coords3d[16*i-16].x, self.coords3d[16*i-12].x, self.coords3d[16*i-8].x, self.coords3d[16*i-4].x,
                self.coords3d[16*i-15].x, self.coords3d[16*i-11].x, self.coords3d[16*i-7].x, self.coords3d[16*i-3].x,
                self.coords3d[16*i-14].x, self.coords3d[16*i-10].x, self.coords3d[16*i-6].x, self.coords3d[16*i-2].x,
                self.coords3d[16*i-13].x, self.coords3d[16*i-9].x, self.coords3d[16*i-5].x, self.coords3d[16*i-1].x]

            ys = [self.coords3d[16*i-16].y, self.coords3d[16*i-15].y, self.coords3d[16*i-14].y, self.coords3d[16*i-13].y,
                self.coords3d[16*i-12].y, self.coords3d[16*i-11].y, self.coords3d[16*i-10].y, self.coords3d[16*i-9].y,
                self.coords3d[16*i-8].y, self.coords3d[16*i-7].y, self.coords3d[16*i-6].y, self.coords3d[16*i-5].y,
                self.coords3d[16*i-4].y, self.coords3d[16*i-3].y, self.coords3d[16*i-2].y, self.coords3d[16*i-1].y]

            zs = [self.coords3d[16*i-16].z, self.coords3d[16*i-15].z, self.coords3d[16*i-14].z, self.coords3d[16*i-13].z,
                self.coords3d[16*i-12].z, self.coords3d[16*i-11].z, self.coords3d[16*i-10].z, self.coords3d[16*i-9].z,
                self.coords3d[16*i-8].z, self.coords3d[16*i-7].z, self.coords3d[16*i-6].z, self.coords3d[16*i-5].z,
                self.coords3d[16*i-4].z, self.coords3d[16*i-3].z, self.coords3d[16*i-2].z, self.coords3d[16*i-1].z]

            gbx = CalculationMatrix('G3D', xs)
            gby = CalculationMatrix('G3D', ys)
            gbz = CalculationMatrix('G3D', zs)
        
        delta = 0.01
        ns = 1 / delta
        eds = CalculationMatrix('delta', delta)

        nt = 1 / delta
        edt = CalculationMatrix('delta', delta)
        
        # TODO: Calcular valores iniciais faltantes e chamar método forward_difference_surface

    def forward_difference_surface(self, ns, nt, cx, cy, cz, eds, edt):
        ddx = eds * cx * edt.translate()
        ddy = eds * cy * edt.translate()
        ddz = eds * cz * edt.translate()
        i = 1
        while (i < ns):
            i += 1
            self.forward_difference_curve(nt, 
                ddx[0][0], ddx[0][1], ddx[0][2], ddx[0][3], 
                ddy[0][0], ddy[0][1], ddy[0][2], ddy[0][3],
                ddz[0][0], ddz[0][1], ddz[0][2], ddz[0][3])
            # TODO: Somar linhas de DD
        ddx = (eds * cx * edt.translate()).translate()
        ddy = (eds * cy * edt.translate()).translate()
        ddz = (eds * cz * edt.translate()).translate()
        i = 1
        while (i < nt):
            i += 1
            self.forward_difference_curve(nt, 
                ddx[0][0], ddx[0][1], ddx[0][2], ddx[0][3], 
                ddy[0][0], ddy[0][1], ddy[0][2], ddy[0][3],
                ddz[0][0], ddz[0][1], ddz[0][2], ddz[0][3])
            # TODO: Somar linhas de DD
        

    def forward_difference_curve(self, n, x, dx, d2x, d3x, y, dy, d2y, d3y, z, dz, d2z, d3z):
        curve_coords = []
        i = 1
        curve_coords.append(Coord(x, y, z))
        while (i < n):
            i += 1

            x += dx
            dx += d2x
            d2x += d3x

            y += dy
            dy += d2y
            d2y += d3y

            z += dz
            dz += d2z
            d2z += d3z

            curve_coords.append(Coord(x, y, z))
        return curve_coords

        