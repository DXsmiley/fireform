import pyglet
import fireform.message
import warnings
import time
import io

############################################### UTILITIES


BLEND_MODES = {
	None: (770, 771),
	'normal': (770, 771),
	'add': (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)
}


############################################### RESOURCE OBJECTS

class image:

	__slots__ = ['image', 'is_smooth', 'flip_cache']

	def __init__(self, file_obj = None, texture = None):
		assert(file_obj or texture)
		if file_obj:
			self.image = pyglet.image.load('hint.png', file = file_obj)
		if texture:
			self.image = texture
		self.is_smooth = False

	@property
	def width(self):
		return self.image.width

	@property
	def height(self):
		return self.image.height

	def smooth(self, smooth = None):
		if smooth is not None:
			self.is_smooth = smooth
		if self.is_smooth:
			warnings.warn('Setting an image to smooth doesn\'t actually affect it.')
		else:
			pyglet.gl.glTexParameteri(self.image.get_texture().target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)

	# Inconsistent with pretty much everything else
	def get_region(self, x, y, w, h):
		texture = self.image.get_region(x, y, w, h)
		i = image(texture = texture)
		i.smooth(self.is_smooth)
		return i

	@property
	def anchor_x(self):
		return self.image.get_texture().anchor_x

	@anchor_x.setter
	def anchor_x(self, value):
		self.image.get_texture().anchor_x = value

	@property
	def anchor_y(self):
		return self.image.get_texture().anchor_y

	@anchor_y.setter
	def anchor_y(self, value):
		self.image.get_texture().anchor_y = value


class image_grid:

	__slots__ = ['grid']

	def __init__(self, image, tiles_x, tiles_y):
		self.grid = pyglet.image.ImageGrid(image.image, tiles_y, tiles_x)

	def get_strip(self, a, b):
		return [image(texture = x) for x in self.grid[a:b]]


class sprite:

	__slots__ = ['sprite']

	def __init__(self, img = None, x = 0, y = 0, batch = None, blend = None):
		# assert(isinstance(batch, fireform.engine.pyglet.batch))
		blend_src, blend_dest = BLEND_MODES.get(blend)
		self.sprite = pyglet.sprite.CroppedSprite(
			img = img.image,
			x = x,
			y = y,
			batch = batch.batch,
			blend_src = blend_src,
			blend_dest = blend_dest
		)

	def set_image(self, value):
		# assert(isinstance(value, image))
		self.sprite.image = value.image
	image = property(fset = set_image)

	def set_x(self, value):
		self.sprite._x = value
	x = property(fset = set_x)

	def set_y(self, value):
		self.sprite._y = value
	y = property(fset = set_y)

	def set_rotation(self, value):
		self.sprite._rotation = value
	rotation = property(fset = set_rotation)

	def set_scale(self, value):
		# TODO: Implement axis-wise scaling once Pyglet supports it.
		# BUG: If the sign of the scale changes at all, the image won't be updated properly.
		if isinstance(value, int) or isinstance(value, float):
			self.sprite._scale_x = value
			self.sprite._scale_y = value
		else:
			x, y = value
			self.sprite._scale_x = x
			self.sprite._scale_y = y
	scale = property(fset = set_scale)

	def get_visible(self):
		return self.sprite._visible

	def set_visible(self, value):
		self.sprite._visible = value
	visible = property(fget = get_visible, fset = set_visible)

	def set_opacity(self, value):
		self.sprite.opacity = value
	opacity = property(fset = set_opacity)

	def set_crop_box(self, value):
		self.sprite.crop_box = value
	crop_box = property(fset = set_crop_box)

	def flush(self):
		self.sprite._update_position()

	def delete(self):
		self.sprite.delete()
		self.sprite = None

class batch:

	__slots__ = ['batch']

	def __init__(self):
		self.batch = pyglet.graphics.Batch()

	def draw(self):
		self.batch.draw()

############################################### TEXT LABELS

class text:

	def __init__(self, **options):
		valid_keys = {'text', 'font_name', 'font_size', 'color', 'x', 'y', 'width', 'multiline'}
		# Text rendering is one of the more complicated things.
		# It's considered OK if the engine does not support all the settings that might get passed to this function
		for i in options:
			if i not in valid_keys:
				warnings.warn('The pyglet engine does not support the {} argument for text objects'.format(i))
		self.opts = options.copy()
		self.label = pyglet.text.Label(
			options.get('text'),
			font_name = options.get('font_name', 'Arial'),
			font_size = options.get('font_size', 10),
			color = options.get('text_colour', (0, 0, 0, 255)),
			x = options.get('x', 8),
			y = options.get('y', 8),
			width = options.get('width', 800),
			multiline = True
		)

	@property
	def text(self):
		return self.opts.get('text', '')

	@text.setter
	def text(self, value):
		if value != self.opts.get('text'):
			self.opts['text'] = value
			self.label.text = value

	@property
	def x(self):
		return self.opts.get('x', '')

	@x.setter
	def x(self, value):
		self.opts['x'] = value
		self.label.x = value

	@property
	def y(self):
		return self.opts.get('y', '')

	@y.setter
	def y(self, value):
		self.opts['y'] = value
		self.label.y = value

	def draw(self):
		self.label.draw()

############################################### DRAWING FUNCTIONS

def draw_set_colour(colour):
	pyglet.gl.glColor4f(*colour)

def draw_lines(lines):
	pyglet.graphics.draw(len(lines) // 2, pyglet.gl.GL_LINES, ('v2f', tuple(lines)))

# TODO: This is *really* slow. Speed it up somehow, possibly making a label object,
# or even a text-rendering system.
def draw_text(**options):
	valid_keys = {'text', 'font_name', 'font_size', 'color', 'x', 'y', 'width', 'multiline'}
	# Text rendering is one of the more complicated things.
	# It's considered OK if the engine does not support all the settings that might get passed to this function
	for i in options:
		if i not in valid_keys:
			warnings.warn('The pyglet engine does not support the {} argument for draw_text'.format(i))
	font_size = options.get('font_size', 10)
	label = pyglet.text.Label(
		options.get('text'),
		font_name = options.get('font_name', 'Arial'),
		font_size = font_size,
		color = options.get('text_colour', (0, 0, 0, 255)),
		x = options.get('x', 8),
		y = options.get('y', 8),
		width = options.get('width', 800),
		multiline = True
	)
	label.draw()

############################################### CAMERA MANIPULATION

# These should impact all subsequent drawing functions.

# Move the camera
def camera_apply(centre_x, centre_y, zoom):
	camera_dispel()
	pyglet.gl.glScalef(zoom, zoom, 1)
	pyglet.gl.glTranslatef(
		int(-centre_x + game_window.width / 2 / zoom),
		int(-centre_y + game_window.height / 2 / zoom),
		0
	)

# Reset the camera to its default position.
def camera_dispel():
	pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
	pyglet.gl.glLoadIdentity()

############################################### INPUT

# import pyglet.window.key as INPUT_KEY_CONSTANTS
# import pyglet.window.mouse as INPUT_MOUSE_CONSTANTS

############################################### SETUP

pyglet.options['debug_gl'] = False

pyglet.resource.path = ['.', './resources']

############################################### MAIN LOOP STUFF

# Nasty hack
w_window_width = 0
w_window_height = 0

mouse_raw_x = 0
mouse_raw_y = 0

last_draw = time.time()
game_window = None
world = None

# Not really sure what this is supposed to be doing, but it appears to be grabbing the
# position of the camera, rather than the mouse :/
def get_mouse_position(world):
	"""Not to be used by mortals."""
	cam_sys = world.systems_by_name.get('fireform.system.camera', None)
	return (0, 0) if cam_sys == None else (cam_sys.cam_x, cam_sys.cam_y)

def get_camera_zoom(world):
	"""Not to be used by mortals."""
	cam_sys = world.systems_by_name.get('fireform.system.camera', None)
	return 1 if cam_sys == None else cam_sys.scale

def run(the_world, window_width = 1280, window_height = 800, clear_colour = (1, 1, 1, 1), show_fps = False, mouse_sensitivity = 1):
	"""Create the window and run the game."""

	global w_window_width
	global w_window_height
	global last_draw
	global game_window
	global world

	world = the_world

	w_window_width = window_width
	w_window_height = window_height

	config = pyglet.gl.Config(sample_buffers = 1, samples = 0, double_buffer = True)
	game_window = pyglet.window.Window(width = window_width, height = window_height, vsync = False, config = config, resizable = True)

	# This prevent the on_draw event being triggered every single time anything happens.
	# It also prevents the flipping of the buffer.
	game_window.invalid = True

	pyglet.gl.glClearColor(*clear_colour)

	def translate_cursor(x, y):
		cx, cy = get_mouse_position(world)
		scale = mouse_sensitivity / get_camera_zoom(world)
		x = (x - w_window_width // 2) * scale + cx
		y = (y - w_window_height // 2) * scale + cy
		return (x, y)

	@game_window.event
	def on_resize(width, height):
		global w_window_width
		global w_window_height
		w_window_width = width
		w_window_height = height
		# print('Window resized to {}, {}'.format(width, height))
		world.handle_message(fireform.message.window_resized(width, height))
		# return pyglet.event.EVENT_HANDLED

	@game_window.event
	def on_key_press(symbol, modifiers):
		# world.handle_message(fireform.message.key_press_targeted(symbol, modifiers))
		world.handle_message(fireform.message.key_press(symbol, modifiers))

	@game_window.event
	def on_key_release(symbol, modifiers):
		# world.handle_message(fireform.message.key_release_targeted(symbol, modifiers))
		world.handle_message(fireform.message.key_release(symbol, modifiers))

	@game_window.event
	def on_mouse_motion(x, y, dx, dy):
		global mouse_raw_x
		global mouse_raw_y
		mouse_raw_x = x
		mouse_raw_y = y
		return pyglet.event.EVENT_HANDLED

	@game_window.event
	def on_mouse_press(x, y, button, modifiers):
		world.handle_message(fireform.message.mouse_click_raw(x, y, button))
		world.handle_message(fireform.message.mouse_click(*translate_cursor(x, y), button))
		return pyglet.event.EVENT_HANDLED

	@game_window.event
	def on_mouse_release(x, y, button, modifiers):
		world.handle_message(fireform.message.mouse_release_raw(x, y, button))
		world.handle_message(fireform.message.mouse_release(*translate_cursor(x, y), button))
		return pyglet.event.EVENT_HANDLED

	@game_window.event
	def on_mouse_drag(x, y, dx, dt, buttons, modifiers):
		# print('on_mouse_drag')
		global mouse_raw_x
		global mouse_raw_y
		mouse_raw_x = x
		mouse_raw_y = y
		return pyglet.event.EVENT_HANDLED

	# This event gets triggered a heck of a lot, and for the worst of reasons (like moving the mouse)
	# Whenever this is called, the GL buffers get flipped.
	# The actual drawing occurs each tick in the update step.
	# @game_window.event
	# def on_draw():
	# 	# print('on_draw()')
	# 	return pyglet.event.EVENT_HANDLED

	TARGET_FPS = 60
	INTERVAL = 1 / TARGET_FPS

	def update(delta_time):
		# if delta_time > INTERVAL or True:
		# 	print('update(', delta_time, ')')
		world.refresh_entities()
		world.handle_message(fireform.message.mouse_move_raw(mouse_raw_x, mouse_raw_y))
		world.handle_message(fireform.message.mouse_move(*translate_cursor(mouse_raw_x, mouse_raw_y)))
		world.handle_message(fireform.message.tick())
		game_window.clear()
		world.handle_message(fireform.message.draw())
		fps_display.draw()
		# game_window.flip()

	fps_display = pyglet.window.FPSDisplay(game_window)
	pyglet.clock.schedule_interval_soft(update, INTERVAL)
	# pyglet.clock.set_fps_limit(TARGET_FPS) # This was depreciated. No longer using it.
	pyglet.app.run()

def swap_world(new_world):
	global world
	old_world = world
	world = new_world
	return old_world

def get_window_width():
	return w_window_width

def get_window_height():
	return w_window_height
