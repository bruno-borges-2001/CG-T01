# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from classes import GraphicObject, Coord, Matrix, CalculationMatrix, GraphicObject3D
from popup import TransformationPopup, Object2DPopup, Object3DPopup
from copy import deepcopy
from math import *

from ioManager import IO

COLORS = {
	"BLACK": "#000000",
	"RED": "#FF0000",
	"GREEN": "#00FF00",
	"BLUE": "#0000FF",
	"DARK RED": "#880000",
	"DARK GREEN": "#008800",
	"DARK BLUE": "#000088",
	"ORANGE": "#FF8800",
	"LIGHT BLUE": "#0088FF",
	"PINK": "#FF0088",
}


class App:
	def __init__(self):
		# WINDOW CONFIG
		self.root = Tk()
		self.root.title("SGI - Interface grafica para insercao de objetos")
		self.root.geometry("1000x600")
		self.root.state('normal')

		# VARIABLE INITIALIZATION
		self.IO = IO()

		self.display_file = []
		self.display_file_normalized = []
		self.display_file_show = []

		self.labels_x = []
		self.entries_x = []
		self.labels_y = []
		self.entries_y = []

		[colors, objs] = self.IO.import_obj()

		COLORS = colors
		self.display_file = objs

		self.padding = 10

		self.window = GraphicObject3D(
			"Window", [Coord(0, 0)], [], COLORS["RED"])
		self.normal_window = GraphicObject("NomalWindow", [
			Coord(-1, -1), Coord(1, -1), Coord(1, 1), Coord(-1, 1)], COLORS["RED"])
		self.viewport = GraphicObject(
			"Viewport", [Coord(0, 0)], COLORS["RED"])

		self.window_rotation_angle_x = 0
		self.window_rotation_angle_y = 0
		self.window_rotation_angle_z = 0

		self.height = 0
		self.width = 0

		# RENDER / UPDATE
		self.render()
		self.root.update_idletasks()
		self.canvas_container.update_idletasks()
		self.canvas.update_idletasks()

	def add_object(self):
		self.add_object_popup = Object2DPopup(
			self.root, self.add_object_on_screen, COLORS)

	def add_object_3D(self):
		self.add_object_3D_popup = Object3DPopup(
			self.root, self.add_object_on_screen, COLORS)

	def add_object_on_screen(self, object_type, name, coords, color, edges=None, object_3D=False):
		if (len(name) > 0 and object_type >= 0):
			if (object_type == 2):
				typeF = "curve"
			elif (object_type == 3):
				typeF = "b_spline_curve"
			elif (object_type == 4):
				typeF = "polygon"
			elif (object_type == 1):
				typeF = "line"
			elif (object_type == 0):
				typeF = "point"

			if (not object_3D):
				new_object = GraphicObject(
					name, coords, COLORS[color], False, typeF)
				self.listbox.insert(END, new_object.name)
				self.log.insert(0, "Object " + new_object.name + " added")
				self.display_file.append(new_object)
				self.draw()
				self.add_object_popup.destroy()
			elif (edges != None and object_3D):
				if (edges and len(edges) == 0 and object_type != 0):
					return
				new_object = GraphicObject3D(
					name, coords, edges, COLORS[color], False)
				self.listbox.insert(END, new_object.name)
				self.log.insert(0, "Object " + new_object.name + " added")
				self.display_file.append(new_object)
				self.draw()
				self.add_object_3D_popup.destroy()

	def check(self, event):
		self.height = self.canvas.winfo_height()
		self.width = self.canvas.winfo_width()

		XWMIN = 0
		YWMIN = 0
		XWMAX = self.width
		YWMAX = self.height

		self.window.coords3d = [
			Coord(XWMIN, YWMIN),
			Coord(XWMIN, YWMAX),
			Coord(XWMAX, YWMAX),
			Coord(XWMAX, YWMIN)
		]

		self.viewport.coords = [
			Coord(XWMIN + self.padding, YWMIN + self.padding),
			Coord(XWMIN + self.padding, YWMAX - self.padding),
			Coord(XWMAX - self.padding, YWMAX - self.padding),
			Coord(XWMAX - self.padding, YWMIN + self.padding)
		]

		self.draw()

	def draw(self):
		self.update_all_points_display_file()
		self.canvas.delete("all")
		aux = []
		for coord in self.viewport.coords:
			aux += coord.to_list()[:-1]
		self.canvas.create_polygon(
			aux, tags="viewport", outline=self.viewport.color, fill="")
		for obj in self.display_file_show:
			for coords in obj.clipped:
				if (len(coords) > 2):
					aux = []
					for coord in coords:
						aux += [coord.x + self.padding,
								coord.y + self.padding]
					if (obj.type == 'polygon'):
						self.canvas.create_polygon(
							aux, tags=obj.name, outline=obj.color, fill="")
					else:
						self.canvas.create_line(
							aux, tags=obj.name, fill=obj.color)
				elif (len(coords) == 2):
					aux = []
					for coord in coords:
						aux += [coord.x + self.padding,
								coord.y + self.padding]
					self.canvas.create_line(
						aux, tags=obj.name, fill=obj.color)
				elif (len(coords) == 1):
					self.canvas.create_oval(
						coords[0].x - 1 + self.padding, coords[0].y - 1 + self.padding, coords[0].x + 1 + self.padding,
						coords[0].y + 1 + self.padding, fill=obj.color)
		self.canvas.tag_raise("viewport")
		self.IO.export_obh(self.display_file, COLORS)

	def generate_scn_matrix(self):
		window_center = self.window.return_center()

		# translation_matrix = CalculationMatrix(
		# 	't', [-(window_center.x), -(window_center.y)])
		translation_matrix = CalculationMatrix('t3D', [-(window_center.x), -(window_center.y), -(window_center.z)])

		# rotation_matrix = CalculationMatrix('r', self.window_rotation_angle_z)
		rotation_matrix = CalculationMatrix('rx3D', self.window_rotation_angle_x) * \
			CalculationMatrix('ry3D', self.window_rotation_angle_y) * \
			CalculationMatrix('rz3D', self.window_rotation_angle_z)
		
		# scale_matrix = CalculationMatrix(
		# 	's', [1 / (self.get_window_width() / 2), 1 / (self.get_window_height() / 2)])
		scale_matrix = CalculationMatrix('s3D', [1 / (self.get_window_width() / 2), 1 / (self.get_window_height() / 2), 1])

		scn_matrix = translation_matrix * rotation_matrix * scale_matrix
		return scn_matrix

	def get_canvas_center(self):
		return Coord(self.width / 2, self.height / 2)

	def get_window_height(self):
		return sqrt(
			(self.window.coords3d[3].x-self.window.coords3d[0].x)**2 +
			(self.window.coords3d[3].y-self.window.coords3d[0].y)**2 +
			(self.window.coords3d[3].z-self.window.coords3d[0].z)**2
		)
		# return self.window.coords3d[2].y - self.window.coords3d[0].y




	def get_window_width(self):
		return sqrt(
			(self.window.coords3d[1].x-self.window.coords3d[0].x)**2 +
			(self.window.coords3d[1].y-self.window.coords3d[0].y)**2 +
			(self.window.coords3d[1].z-self.window.coords3d[0].z)**2
		)

	def get_translate_values(self, direction):
		value = self.get_window_height() * 0.1
		if (direction == 'up'):
			return (0, value, 0)
		elif (direction == 'down'):
			return (0, -value, 0)
		elif (direction == 'left'):
			return (-value, 0, 0)
		elif (direction == 'right'):
			return (value, 0, 0)

	def get_viewport_coords(self, wcoords):
		min_wcoords = self.normal_window.coords[0]
		max_wcoords = self.normal_window.coords[2]
		min_vpcoords = self.viewport.coords[0]
		max_vpcoords = self.viewport.coords[2]
		x = (wcoords.x - min_wcoords.x) * (max_vpcoords.x -
										   min_vpcoords.x) / (max_wcoords.x - min_wcoords.x)
		y = (1 - ((wcoords.y - min_wcoords.y) / (max_wcoords.y -
												 min_wcoords.y))) * (max_vpcoords.y - min_vpcoords.y)
		return Coord(x, y)

	def handle_action_click(self, action):
		selection = self.listbox.curselection()
		if len(selection) > 0:
			self.popup = TransformationPopup(
				self.root, action, selection[0], lambda item, values: self.handle_submit(item, action, values))

	def handle_clear_selection(self):
		self.listbox.select_clear(0, END)

	def handle_submit(self, item, action, values):
		if action == "Translação":
			self.display_file[item].translate(*values[:3])
		elif action == "Rotação":
			origin = Coord(0, 0, 0)
			if values[4] == 2 or values[4] == 4 or values[4] == 5 or values[4] == 6:
				origin = self.display_file[item].return_center()
			elif values[4] == 3:
				origin = Coord(*values[:3])
			angle = values[3]
			if values[4] == 4:
				self.display_file[item].rotate_x(origin.x, origin.y, origin.z, angle)
			elif values[4] == 5:
				self.display_file[item].rotate_y(origin.x, origin.y, origin.z, angle)
			elif values[4] == 6:
				self.display_file[item].rotate_z(origin.x, origin.y, origin.z, angle)
			else:
				self.display_file[item].rotate(origin.x, origin.y, origin.z, angle)
		elif action == "Escala":
			self.display_file[item].center_scale(*values[:3])
		self.popup.destroy()
		self.draw()

	def handle_translation(self, direction):
		selected = self.listbox.curselection()
		if len(selected) > 0:
			values = self.get_translate_values(direction)
			for item in selected:
				self.log.insert(
					0, "Object " + self.display_file[item].name + " moved " + direction)
				self.display_file[item].translate(*values)
			self.draw()
		else:
			self.move_window(direction)

	def handle_window_rotation(self, direction):
		self.window_rotation_angle_z += 15 if direction == 'right' else -15
		# self.window.center_rotate(self.window_rotation_angle_z, 'z')
		self.log.insert(0, "Window rotated " + direction + " on axis z")
		# self.log.insert(0, "Window rotated " + direction)
		self.draw()

	def window_rotation(self, direction, axis):
		if (axis == 'x'):
			self.window_rotation_angle_x += 15 if direction == 'top' else -15
			#self.window.center_rotate(self.window_rotation_angle_x, axis)
		elif (axis == 'y'):
			self.window_rotation_angle_y += 15 if direction == 'right' else -15
			#self.window.center_rotate(self.window_rotation_angle_y, axis)

		self.log.insert(0, "Window rotated " + direction + " on axis " + axis)
		self.draw()

	def handle_zoom(self, signal):
		selected = self.listbox.curselection()
		if len(selected) > 0:
			zoom = 1.1 if signal > 0 else 0.9
			for item in selected:
				self.log.insert(
					0, "Object " + self.display_file[item].name + " zoomed " + ("in" if signal > 0 else "out"))
				self.display_file[item].center_scale(zoom, zoom, 1)
			self.draw()
		else:
			self.zoom(signal)

	def move_window(self, direction):
		Cx = 0
		Cy = 0
		if (direction == 'up'):
			Cy = self.get_window_height() * 0.1
		elif (direction == 'down'):
			Cy = -self.get_window_height() * 0.1
		elif (direction == "left"):
			Cx = -self.get_window_height() * 0.1
		elif (direction == 'right'):
			Cx = self.get_window_height() * 0.1
		self.window.translate(Cx, Cy, 0)
		self.log.insert(0, "Window moved " + direction)
		self.draw()

	def normalize_display_file(self):
		scn_matrix = self.generate_scn_matrix()
		graphic_objects = deepcopy(self.display_file)

		#self.parallel_projection()
		self.perspective_projection()

		self.display_file_normalized = []
		for graphic_object in graphic_objects:
			aux = []
			for coord in graphic_object.coords:
				result = CalculationMatrix('c3d', coord.to_list()) * scn_matrix
				aux.append(Coord(*result.matrix[0]))
			graphic_object.coords = aux
			graphic_object.normalized = True
			self.display_file_normalized.append(graphic_object)

	def parallel_projection(self):
		vrp = self.window.return_center()
		vrpt = Coord(*(CalculationMatrix('c3d', vrp.to_list()) *
					   CalculationMatrix('t3D', (vrp * -1).to_list())).matrix[0][:-1])
		p1 = vrpt - self.window.coords3d[0] - vrp
		p2 = self.window.coords3d[1] - vrp - vrpt
		vpn = Coord(p1.y * p2.z - p1.z * p2.y, p1.z * p2.x -
					p1.x * p2.z, p1.x * p2.y - p1.y * p2.x)
		teta_x = atan(vpn.y / vpn.z)
		teta_y = atan(vpn.x / vpn.z)
		self.window.projection(vrp, vpn, teta_x, teta_y, 'parallel')
		for obj in self.display_file:
			if (type(obj) is GraphicObject3D):
				obj.projection(vrp, vpn, teta_x, teta_y, 'parallel')

	def perspective_projection(self):
		vision_angle = 120
		cop_distance = abs(self.get_window_width() / tan(vision_angle))
		vrp = self.window.return_center()
		vrpt = Coord(*(CalculationMatrix('c3d', vrp.to_list()) *
					   CalculationMatrix('t3D', (vrp * -1).to_list())).matrix[0][:-1])
		p1 = vrpt - deepcopy(self.window.coords3d[0]) - vrp
		p2 = deepcopy(self.window.coords3d[1]) - vrp - vrpt
		vpn = Coord(p1.y * p2.z - p1.z * p2.y, p1.z * p2.x -
					p1.x * p2.z, p1.x * p2.y - p1.y * p2.x)
		teta_x = atan(vpn.y / vpn.z)
		teta_y = atan(vpn.x / vpn.z)
		self.window.projection(vrp, vpn, teta_x, teta_y, 'perspective', cop_distance)
		for obj in self.display_file:
			if (type(obj) is GraphicObject3D):
				obj.projection(vrp, vpn, teta_x, teta_y, 'perspective', cop_distance)

	def remove_object(self):
		self.log.insert(
			0, "Object " + self.listbox.get(self.listbox.curselection()) + " removed")
		self.canvas.delete(self.listbox.get(self.listbox.curselection()))
		self.display_file.pop(self.listbox.curselection()[0])
		self.listbox.delete(self.listbox.curselection())
		self.draw()

	def render(self):
		function_container = Frame(self.root, width=30)
		function_container.pack(side=LEFT, fill=Y)

		Label(function_container, text="Funções", width=30).pack(side=TOP)

		self.listbox = Listbox(function_container, width=35, selectmode=SINGLE)
		self.listbox.pack(side=TOP)

		for o in self.display_file:
			self.listbox.insert(END, o.name)

		Button(function_container, width=29, text="Limpar",
			   command=self.handle_clear_selection).pack(side=TOP)

		add_and_remove_container = Frame(function_container)
		add_and_remove_container.pack(side=TOP, pady=10)

		container_3d = Frame(function_container)
		container_3d.pack(side=TOP)

		Label(function_container,
			  text="Window/Objeto (selecione na listbox)", width=30).pack(side=TOP, pady=10)

		main_button_container = Frame(function_container, width=35)
		main_button_container.pack(side=TOP)

		arrows_container = Frame(main_button_container, padx=10)
		arrows_container.pack(side=LEFT)

		up_container = Frame(arrows_container)
		up_container.pack(side=TOP)

		directions_container = Frame(arrows_container)
		directions_container.pack(side=TOP)

		zoom_container = Frame(main_button_container)
		zoom_container.pack(side=RIGHT, pady=10, padx=10)

		object_actions_container = Frame(function_container)
		object_actions_container.pack(side=TOP)

		rotation_container = Frame(function_container)
		rotation_container.pack(side=TOP, pady=10)

		self.canvas_container = Frame(self.root)
		self.canvas_container.pack(fill=BOTH, expand=True)

		self.canvas = Canvas(self.canvas_container, background="white")
		self.canvas.pack(fill=BOTH, expand=True)

		self.canvas.bind("<Configure>", self.check)

		Button(add_and_remove_container, text="Adicionar Objeto",
			   command=self.add_object).pack(side=LEFT)

		Button(add_and_remove_container, text="Remover Objeto",
			   command=self.remove_object).pack(side=RIGHT)

		Button(container_3d, text="Adicionar Objeto 3D",
			   command=self.add_object_3D).pack(side=BOTTOM)

		Button(up_container, text="↑",
			   command=lambda: self.handle_translation('up')).pack(side=TOP)

		Button(directions_container, text="←",
			   command=lambda: self.handle_translation('left')).pack(side=LEFT)

		Button(directions_container, text="↓",
			   command=lambda: self.handle_translation('down')).pack(side=LEFT)

		Button(directions_container, text="→",
			   command=lambda: self.handle_translation('right')).pack(side=LEFT)

		Button(zoom_container, text="+",
			   command=lambda: self.handle_zoom(1)).pack()

		Button(zoom_container, text="-",
			   command=lambda: self.handle_zoom(-1)).pack()

		Button(object_actions_container, text="Translação",
			   command=lambda: self.handle_action_click("Translação")).pack(side=LEFT)

		Button(object_actions_container, text="Rotação",
			   command=lambda: self.handle_action_click("Rotação")).pack(side=LEFT)

		Button(object_actions_container, text="Escala",
			   command=lambda: self.handle_action_click("Escala")).pack(side=LEFT)

		Button(rotation_container, text="↶",
			   command=lambda: self.handle_window_rotation('left')).pack(side=LEFT)

		Button(rotation_container, text="↷",
			   command=lambda: self.handle_window_rotation('right')).pack(side=LEFT)

		Button(rotation_container, text="↻",
			   command=lambda: self.window_rotation('left', 'y')).pack(side=LEFT)

		Button(rotation_container, text="↺",
			   command=lambda: self.window_rotation('right', 'y')).pack(side=LEFT)

		Button(rotation_container, text="⤴",
			   command=lambda: self.window_rotation('top', 'x')).pack(side=LEFT)

		Button(rotation_container, text="⤵",
			   command=lambda: self.window_rotation('bottom', 'x')).pack(side=LEFT)

		self.log = Listbox(function_container, width=35)
		self.log.pack(fill=Y, side=BOTTOM)

	def start_app(self):
		self.root.mainloop()

	def transform_coords(self, coords):
		aux = []
		for coord in coords:
			aux.append(self.get_viewport_coords(coord))
		return aux

	def update_all_points_display_file(self):
		self.normalize_display_file()
		self.display_file_show = []
		for normalized_object in self.display_file_normalized:
			aux = deepcopy(normalized_object)
			if (len(aux.coords) == 1):
				aux.clip_point()
			elif (len(aux.coords) == 2):
				aux.clip_line()
			elif (len(aux.coords) > 2):
				if (aux.type == 'curve' or aux.type == 'b_spline_curve' or aux.type == 'line'):
					aux.clip_curve()
				else:
					aux.clip_polygon()
			clipped_aux = []
			for obj in aux.clipped:
				if (len(obj) == 1):
					clipped_aux.append(obj)
					continue
				aux_edge = deepcopy(obj)
				for i in [0, 1]:
					if (type(obj[i]) is not Coord):
						aux_edge[i] = aux.coords[obj[i]]
				clipped_aux.append(aux_edge)

			aux.clipped = list(map(self.transform_coords, clipped_aux))
			self.display_file_show.append(aux)

	def zoom(self, signal):
		zoom_value = 0.9 if signal > 0 else 1.1
		self.window.center_scale(zoom_value, zoom_value, 1)
		self.log.insert(0, "zoomed in" if signal > 0 else "zoomed out")
		self.draw()
