from fireform.system.base import base
import fireform.data
import fireform.main
import time
import collections

def stats_factory():
	return collections.defaultdict(stats_factory)

def indent(string):
	lines = string.strip('\n').split('\n')
	for i in range(len(lines)):
		lines[i] = '    ' + lines[i]
	return '\n'.join(lines) + '\n'

def format_stats_small(s):
	if type(s) in [tuple, list, set]:
		return '(' + ', '.join(map(format_stats_small, s)) + ')'
	elif type(s) in [float, int]:
		return '{:.2f}'.format(s)
	else:
		return str(s)

def format_stats(s):
	result = ''
	for k, v in s.items():
		if isinstance(v, dict):
			result += k + ':\n' + indent(format_stats(v))
		else:
			result += '{}: {}\n'.format(k, format_stats_small(v))
	return result

class debug(base):
	"""Usefull for debugging.

	Draws boxes around objects that have a position and size."""

	def __init__(self, **kwargs):
		self.text_colour = kwargs.get('text_colour', (0, 0, 0, 255))
		self.outline_colour = kwargs.get('outline_colour', (0, 0.8, 0, 1))
		self.outline_colour_solid = kwargs.get('outline_colour_solid', (0, 1, 0, 1))
		self.outline_colour_hover = kwargs.get('outline_colour_hover', (0, 1, 1, 1))
		self.outline_colour_error = kwargs.get('outline_colour_error', (1, 0.2, 0, 1))
		self.allow_edit = kwargs.get('allow_edit', False)
		self.enable_console = kwargs.get('enable_console', self.allow_edit)
		self.display_things = kwargs.get('display', True)
		self.mouse_x = 0
		self.mouse_y = 0
		self.mouse_x_last = 0
		self.mouse_y_last = 0
		self.selected = False
		self.targeted = None
		self.scaling = False
		self.typing = False
		self.text_input = ''
		self.console_log = ''
		self.filter = None
		self.start_time = time.time()
		self.stats = stats_factory()
		self.set_stat('mouse', (0, 0))
		self.set_stat('mouse raw', (0, 0))
		self.set_stat('time.ticks', 0)
		self.set_stat('time.real', 0)
		self.set_stat('entities.alive', 0)
		self.set_stat('entities.dead', 0)
		self.set_stat('entities.on screen', 0)
		self.text_label = fireform.engine.current.text(
			text = '',
			font_name = 'Courier New',
			font_size = 10,
			color = self.text_colour,
			x = 8,
			multiline = True
		)
		self.camera_system = None

	def set_stat(self, key, value):
		stack = key.split('.')[::-1]
		scope = self.stats
		while len(stack) > 1:
			scope = scope[stack.pop()]
		scope[stack[0]] = value

	def attach(self, world):
		self.filter = world.filter_root.chain('box > -#no-debug')
		self.camera_system = world.systems_by_name['fireform.system.camera']

	def display_menu(self):
		the_text = format_stats(self.stats) + '\n'
		if self.allow_edit and self.targeted:
			the_text += 'Entity selected:\n' + str(self.targeted)
		else:
			the_text += 'Nothing selected'
		the_text += '\n\n' + self.console_log
		if self.typing:
			the_text += '\n\n>>> ' + self.text_input
		self.text_label.text = the_text
		self.text_label.draw()

	def execute_command(self, world, command):
		try:
			# import fireform as ff
			e = self.targeted
			exec(command)
		except Exception as error:
			self.console_log += str(error) + '\n'

	def m_new_entity(self, world, message):
		self.stats['entities']['alive'] += 1

	def m_dead_entity(self, world, message):
		self.stats['entities']['alive'] -= 1
		self.stats['entities']['dead'] += 1

	def m_key_press(self, world, message):
		# if self.allow_edit:
		# 	if self.typing:
		# 		if message.key == fireform.input.key.RETURN:
		# 			self.execute_command(world, self.text_input)
		# 			self.typing = False
		# 			self.text_input = ''
		# 			print('Not typing now!')
		# 		elif message.key == fireform.input.key.BACKSPACE:
		# 			self.text_input = self.text_input[:-1]
		# 		elif 32 <= message.key < 127:
		# 			self.text_input += chr(message.key)
		# 	else:
		# 		if message.key == fireform.input.key.RETURN:
		# 			self.typing = True
		# 			print('Typing now!')
		if message.key == fireform.input.key.TAB:
			self.display_things = not self.display_things

	def find_targeted(self, world):
		best = None
		for i in self.filter:
			x1 = i.box.left
			x2 = i.box.right
			y1 = i.box.bottom
			y2 = i.box.top
			# Check bounds
			if min(x1, x2) <= self.mouse_x <= max(x1, x2) and min(y1, y2) <= self.mouse_y <= max(y1, y2):
				if best == None or i.box.area < best.box.area:
					best = i
		return best

	def m_mouse_move(self, world, message):
		self.set_stat('mouse', (message.x, message.y))
		if self.allow_edit:
			self.mouse_x = message.x
			self.mouse_y = message.y
			if self.selected:
				if self.scaling:
					self.targeted.box.size.x += self.mouse_x - self.mouse_x_last
					self.targeted.box.size.y += self.mouse_y - self.mouse_y_last
					# self.targeted.box.size.x = max(self.targeted.box.size.x, 2)
					# self.targeted.box.size.y = max(self.targeted.box.size.y, 2)
				else:
					self.targeted.box.position.x += self.mouse_x - self.mouse_x_last
					self.targeted.box.position.y += self.mouse_y - self.mouse_y_last
			else:
				self.targeted = self.find_targeted(world)
			self.mouse_x_last = message.x
			self.mouse_y_last = message.y

	def m_mouse_move_raw(self, world, message):
		self.set_stat('mouse raw', (message.x, message.y))

	def m_mouse_click(self, world, message):
		if self.allow_edit:
			if self.targeted and self.display_things:
				self.selected = not self.selected
				self.scaling = message.button == fireform.input.mouse.RIGHT

	def m_window_resized(self, world, message):
		self.text_label.y = message.height - 20

	def m_tick(self, world, message):
		# This will work because we know that these stats have been set up at the start
		self.stats['time']['ticks'] += 1
		self.stats['time']['real'] = (time.time() - self.start_time) * 60

	def m_update_tracked_value(self, world, message):
		self.set_stat(message.key, message.value)

	def name(self):
		return 'fireform.system.debug'

	def m_draw(self, world, message):
		bounds = self.camera_system.boundary()
		if self.display_things:
			# Draw entity collision boxes
			points_nonspecial = []
			points_error = []
			points_solid = []
			points_hover = []
			self.stats['entities']['on screen'] = 0
			for i in self.filter:
				rect = i[fireform.data.box].rectangle
				if fireform.geom.box_overlap(bounds, rect):
					self.stats['entities']['on screen'] += 1
					pos = i[fireform.data.box].position
					points = [
						# Rectangle
						rect.left,
						rect.bottom,
						rect.left,
						rect.top,

						rect.left,
						rect.top,
						rect.right,
						rect.top,

						rect.right,
						rect.top,
						rect.right,
						rect.bottom,

						rect.right,
						rect.bottom,
						rect.left,
						rect.bottom,

						# Origin
						pos.x - 2,
						pos.y - 2,
						pos.x + 2,
						pos.y + 2,

						pos.x + 2,
						pos.y - 2,
						pos.x - 2,
						pos.y + 2
					]
					if rect.left > rect.right or rect.bottom > rect.top:
						points_error += points
					elif i == self.targeted:
						points_hover += points
					elif i[fireform.data.solid] or 'solid' in i.tags:
						points_solid += points
					else:
						points_nonspecial += points

			if points_nonspecial:
				fireform.engine.current.draw_set_colour(self.outline_colour)
				fireform.engine.current.draw_lines(points_nonspecial)
			if points_error:
				fireform.engine.current.draw_set_colour(self.outline_colour_error)
				fireform.engine.current.draw_lines(points_error)
			if points_solid:
				fireform.engine.current.draw_set_colour(self.outline_colour_solid)
				fireform.engine.current.draw_lines(points_solid)
			if points_hover:
				fireform.engine.current.draw_set_colour(self.outline_colour_hover)
				fireform.engine.current.draw_lines(points_hover)

			# I feel like there should be a better way of implementing layers.
			# TODO: Manually dispelling the matrix is nasty.
			# Create a draw_gui event like in GameMaker.
			world.post_message(fireform.system.camera_dispel_matrix())
			self.display_menu()
			# self.fps.draw()
			world.post_message(fireform.system.camera_apply_matrix())
