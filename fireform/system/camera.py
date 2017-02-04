from fireform.system.base import base
import fireform.message
import fireform.data

def triangles(l, t, r, b):
	return [
		l, t,
		r, t,
		l, b,
		r, t,
		l, b,
		r, b
	]

class camera_moved(fireform.message.base):

	name = 'camera_moved'

	def __init__(self, x, y, scale, boundary):
		self.boundary = boundary
		self.x = x
		self.y = y
		self.scale = scale

	def name(self):
		return 'camera_moved'

class camera(base):
	"""Shove this in your world for cameras to work.

	You probably want cameras to work."""

	def __init__(self, letterbox = False):
		# self.message_handles = {
		# 	'draw': self.m_draw,
		# 	'window_resized': self.m_window_resized,
		# 	'camera_apply_matrix': self.m_camera_apply_matrix
		# }
		self.cam_num = 0
		self.cam_x = 0
		self.cam_y = 0
		self.window_width = 128
		self.window_height = 128
		self.scale = 1
		self.letterbox = True
		self.filter = None
		# Currently used to implement the debug system's panning while world is frozen.
		self.forced_offset_x = 0
		self.forced_offset_y = 0
		self.forced_offset_scale = 1

	def name(self):
		return 'fireform.system.camera'

	def attach(self, world):
		self.filter = world.filter_root.chain('box > camera')

	def apply_matrix(self):
		fireform.engine.current.camera_apply(self.cam_x, self.cam_y, self.scale)

	def draw_letterbox():
		pass

	def boundary(self):
		return fireform.geom.rectangle(
			self.cam_x - (self.window_width / 2 / self.scale),
			self.cam_y - (self.window_height / 2 / self.scale),
			self.cam_x + (self.window_width / 2 / self.scale),
			self.cam_y + (self.window_height / 2 / self.scale)
		)

	@fireform.message.surpass_frozen
	def m_tick(self, world, message):
		world.handle_message(camera_moved(self.cam_x, self.cam_y, self.scale, self.boundary()))

	@fireform.message.surpass_frozen
	def m_draw(self, world, message):
		self.cam_num = 0
		self.cam_x = 0
		self.cam_y = 0
		self.scale = 0
		for i in self.filter:
			pos = i[fireform.data.box]
			cam = i[fireform.data.camera]
			self.cam_num += cam.weight
			self.cam_x += pos.x * cam.weight
			self.cam_y += pos.y * cam.weight
			self.scale += cam.zoom * cam.weight
		if self.cam_num == 0:
			self.cam_num = 1
			self.scale = 1
		self.cam_x //= self.cam_num
		self.cam_y //= self.cam_num
		self.scale /= self.cam_num
		self.cam_x += int(self.forced_offset_x)
		self.cam_y += int(self.forced_offset_y)
		self.scale *= self.forced_offset_scale
		world.handle_message(camera_moved(self.cam_x, self.cam_y, self.scale, self.boundary()))
		self.apply_matrix()

	@fireform.message.surpass_frozen
	def m_window_resized(self, world, message):
		self.window_width = message.width
		self.window_height = message.height

	@fireform.message.surpass_frozen
	def m_camera_apply_matrix(self, world, message):
		self.apply_matrix()

	@fireform.message.surpass_frozen
	def m_camera_dispel_matrix(self, world, message):
		fireform.engine.current.camera_dispel()

def camera_apply_matrix():
	return fireform.message.generic('camera_apply_matrix')

def camera_dispel_matrix():
	return fireform.message.generic('camera_dispel_matrix')
