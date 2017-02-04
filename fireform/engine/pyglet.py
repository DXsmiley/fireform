import pyglet
import pyglet.image
import fireform.message
import warnings
import time
import io
import math

############################################### Pyglet Replacements

class PygletSprite(pyglet.sprite.Sprite):
	"""Used instead of pyglet's inbuilt sprite until
	"""
	_batch = None
	_animation = None
	_rotation = 0
	_opacity = 255
	_rgb = (255, 255, 255)
	_scale = 1.0
	_scale_x = 1.0
	_scale_y = 1.0
	_visible = True
	_vertex_list = None

	def __init__(self,
				 img, x=0, y=0,
				 blend_src=pyglet.gl.GL_SRC_ALPHA,
				 blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
				 batch=None,
				 group=None,
				 usage='dynamic',
				 subpixel=False):
		'''Create a sprite.

		:Parameters:
			`img` : `AbstractImage` or `Animation`
				Image or animation to display.
			`x` : int
				X coordinate of the sprite.
			`y` : int
				Y coordinate of the sprite.
			`blend_src` : int
				OpenGL blend source mode.  The default is suitable for
				compositing sprites drawn from back-to-front.
			`blend_dest` : int
				OpenGL blend destination mode.  The default is suitable for
				compositing sprites drawn from back-to-front.
			`batch` : `Batch`
				Optional batch to add the sprite to.
			`group` : `Group`
				Optional parent group of the sprite.
			`usage` : str
				Vertex buffer object usage hint, one of ``"none"``,
				``"stream"``, ``"dynamic"`` (default) or ``"static"``.  Applies
				only to vertex data.
			`subpixel` : bool
				Allow floating-point coordinates for the sprite. By default,
				coordinates are restricted to integer values.

		'''
		if batch is not None:
			self._batch = batch

		self._x = x
		self._y = y

		if isinstance(img, pyglet.image.Animation):
			self._animation = img
			self._frame_index = 0
			self._texture = img.frames[0].image.get_texture()
			self._next_dt = img.frames[0].duration
			if self._next_dt:
				clock.schedule_once(self._animate, self._next_dt)
		else:
			self._texture = img.get_texture()

		self._group = pyglet.sprite.SpriteGroup(self._texture, blend_src, blend_dest, group)
		self._usage = usage
		self._subpixel = subpixel
		self._create_vertex_list()

	def __del__(self):
		try:
			if self._vertex_list is not None:
				self._vertex_list.delete()
		except:
			pass

	def delete(self):
		'''Force immediate removal of the sprite from video memory.

		This is often necessary when using batches, as the Python garbage
		collector will not necessarily call the finalizer as soon as the
		sprite is garbage.
		'''
		if self._animation:
			clock.unschedule(self._animate)
		self._vertex_list.delete()
		self._vertex_list = None
		self._texture = None

		# Easy way to break circular reference, speeds up GC
		self._group = None

	def _animate(self, dt):
		self._frame_index += 1
		if self._frame_index >= len(self._animation.frames):
			self._frame_index = 0
			self.dispatch_event('on_animation_end')
			if self._vertex_list is None:
				return # Deleted in event handler.

		frame = self._animation.frames[self._frame_index]
		self._set_texture(frame.image.get_texture())

		if frame.duration is not None:
			duration = frame.duration - (self._next_dt - dt)
			duration = min(max(0, duration), frame.duration)
			clock.schedule_once(self._animate, duration)
			self._next_dt = duration
		else:
			self.dispatch_event('on_animation_end')

	def _set_batch(self, batch):
		if self._batch == batch:
			return

		if batch is not None and self._batch is not None:
			self._batch.migrate(self._vertex_list, GL_QUADS, self._group, batch)
			self._batch = batch
		else:
			self._vertex_list.delete()
			self._batch = batch
			self._create_vertex_list()

	def _get_batch(self):
		return self._batch

	batch = property(_get_batch, _set_batch,
					 doc='''Graphics batch.

	The sprite can be migrated from one batch to another, or removed from its
	batch (for individual drawing).  Note that this can be an expensive
	operation.

	:type: `Batch`
	''')

	def _set_group(self, group):
		if self._group.parent == group:
			return

		self._group = SpriteGroup(self._texture,
								  self._group.blend_src,
								  self._group.blend_dest,
								  group)

		if self._batch is not None:
			self._batch.migrate(self._vertex_list, GL_QUADS, self._group,
								self._batch)

	def _get_group(self):
		return self._group.parent

	group = property(_get_group, _set_group,
					 doc='''Parent graphics group.

	The sprite can change its rendering group, however this can be an
	expensive operation.

	:type: `Group`
	''')

	def _get_image(self):
		if self._animation:
			return self._animation
		return self._texture

	def _set_image(self, img):
		if self._animation is not None:
			clock.unschedule(self._animate)
			self._animation = None

		if isinstance(img, pyglet.image.Animation):
			self._animation = img
			self._frame_index = 0
			self._set_texture(img.frames[0].image.get_texture())
			self._next_dt = img.frames[0].duration
			if self._next_dt:
				clock.schedule_once(self._animate, self._next_dt)
		else:
			self._set_texture(img.get_texture())
		self._update_position()

	image = property(_get_image, _set_image,
					 doc='''Image or animation to display.

	:type: `AbstractImage` or `Animation`
	''')

	def _set_texture(self, texture):
		if texture.id is not self._texture.id:
			self._group = pyglet.sprite.SpriteGroup(texture,
									  self._group.blend_src,
									  self._group.blend_dest,
									  self._group.parent)
			if self._batch is None:
				self._vertex_list.tex_coords[:] = texture.tex_coords
			else:
				self._vertex_list.delete()
				self._texture = texture
				self._create_vertex_list()
		else:
			self._vertex_list.tex_coords[:] = texture.tex_coords
		self._texture = texture

	def _create_vertex_list(self):
		if self._subpixel:
			vertex_format = 'v2f/%s' % self._usage
		else:
			vertex_format = 'v2i/%s' % self._usage
		if self._batch is None:
			self._vertex_list = graphics.vertex_list(4,
				vertex_format,
				'c4B', ('t3f', self._texture.tex_coords))
		else:
			self._vertex_list = self._batch.add(4, pyglet.gl.GL_QUADS, self._group,
				vertex_format,
				'c4B', ('t3f', self._texture.tex_coords))
		self._update_position()
		self._update_color()

	def _update_position(self):
		img = self._texture
		if not self._visible:
			vertices = [0, 0, 0, 0, 0, 0, 0, 0]
		elif self._rotation:
			x1 = -img.anchor_x * self._scale_x
			y1 = -img.anchor_y * self._scale_y
			x2 = x1 + img.width * self._scale_x
			y2 = y1 + img.height * self._scale_y
			x = self._x
			y = self._y

			r = -math.radians(self._rotation)
			cr = math.cos(r)
			sr = math.sin(r)
			ax = x1 * cr - y1 * sr + x
			ay = x1 * sr + y1 * cr + y
			bx = x2 * cr - y1 * sr + x
			by = x2 * sr + y1 * cr + y
			cx = x2 * cr - y2 * sr + x
			cy = x2 * sr + y2 * cr + y
			dx = x1 * cr - y2 * sr + x
			dy = x1 * sr + y2 * cr + y
			vertices = [ax, ay, bx, by, cx, cy, dx, dy]
		elif self._scale_x != 1.0 or self._scale_y != 1.0:
			x1 = self._x - img.anchor_x * self._scale_x
			y1 = self._y - img.anchor_y * self._scale_y
			x2 = x1 + img.width * self._scale_x
			y2 = y1 + img.height * self._scale_y
			vertices = [x1, y1, x2, y1, x2, y2, x1, y2]
		else:
			x1 = self._x - img.anchor_x
			y1 = self._y - img.anchor_y
			x2 = x1 + img.width
			y2 = y1 + img.height
			vertices = [x1, y1, x2, y1, x2, y2, x1, y2]
		if not self._subpixel:
			vertices = [int(v) for v in vertices]
		self._vertex_list.vertices[:] = vertices

	def _update_color(self):
		r, g, b = self._rgb
		self._vertex_list.colors[:] = [r, g, b, int(self._opacity)] * 4

	def set_position(self, x, y):
		'''Set the X and Y coordinates of the sprite simultaneously.

		:Parameters:
			`x` : int
				X coordinate of the sprite.
			`y` : int
				Y coordinate of the sprite.

		'''
		self._x = x
		self._y = y
		self._update_position()

	position = property(lambda self: (self._x, self._y),
						lambda self, t: self.set_position(*t),
						doc='''The (x, y) coordinates of the sprite.

	:type: (int, int)
	''')

	def _set_x(self, x):
		self._x = x
		self._update_position()

	x = property(lambda self: self._x, _set_x,
				 doc='''X coordinate of the sprite.

	:type: int
	''')

	def _set_y(self, y):
		self._y = y
		self._update_position()

	y = property(lambda self: self._y, _set_y,
				 doc='''Y coordinate of the sprite.

	:type: int
	''')

	def _set_rotation(self, rotation):
		self._rotation = rotation
		self._update_position()

	rotation = property(lambda self: self._rotation, _set_rotation,
						doc='''Clockwise rotation of the sprite, in degrees.

	The sprite image will be rotated about its image's (anchor_x, anchor_y)
	position.

	:type: float
	''')

	def _set_scale(self, scale):
		if isinstance(scale, tuple):
			self._scale_x, self._scale_y = scale
		else:
			self._scale_x = self._scale_y = scale
		self._update_position()

	scale = property(lambda self: self._scale, _set_scale,
					 doc='''Scaling factor.

	A scaling factor of 1 (the default) has no effect.  A scale of 2 will draw
	the sprite at twice the native size of its image.

	:type: float
	''')

	def _get_width(self):
		if self._subpixel:
			return self._texture.width * abs(self._scale_x)
		else:
			return int(self._texture.width * abs(self._scale_x))

	width = property(_get_width,
					 doc='''Scaled width of the sprite.

	Read-only.  Invariant under rotation.

	:type: int
	''')

	def _get_height(self):
		if self._subpixel:
			return self._texture.height * abs(self._scale_y)
		else:
			return int(self._texture.height * abs(self._scale_y))

	height = property(_get_height,
					  doc='''Scaled height of the sprite.

	Read-only.  Invariant under rotation.

	:type: int
	''')

	def _set_opacity(self, opacity):
		self._opacity = opacity
		self._update_color()

	opacity = property(lambda self: self._opacity, _set_opacity,
					   doc='''Blend opacity.

	This property sets the alpha component of the colour of the sprite's
	vertices.  With the default blend mode (see the constructor), this
	allows the sprite to be drawn with fractional opacity, blending with the
	background.

	An opacity of 255 (the default) has no effect.  An opacity of 128 will
	make the sprite appear translucent.

	:type: int
	''')

	def _set_color(self, rgb):
		self._rgb = map(int, rgb)
		self._update_color()

	color = property(lambda self: self._rgb, _set_color,
					   doc='''Blend color.

	This property sets the color of the sprite's vertices. This allows the
	sprite to be drawn with a color tint.

	The color is specified as an RGB tuple of integers ``(red, green, blue)``.
	Each color component must be in the range 0 (dark) to 255 (saturated).

	:type: (int, int, int)
	''')

	def _set_visible(self, visible):
		self._visible = visible
		self._update_position()

	visible = property(lambda self: self._visible, _set_visible,
					   '''True if the sprite will be drawn.

	:type: bool
	''')

	def draw(self):
		'''Draw the sprite at its current position.

		See the module documentation for hints on drawing multiple sprites
		efficiently.
		'''
		self._group.set_state_recursive()
		self._vertex_list.draw(GL_QUADS)
		self._group.unset_state_recursive()

def clamp(value, minimum, maximum):
	return max(min(value, maximum), minimum)

def mir_lerp(start, end, from_start, from_end, value):
	perc = float(value - from_start) / float(from_end - from_start)
	perc = clamp(perc, 0.0, 1.0)
	return start + (end - start) * perc

class CroppedSprite(PygletSprite):

	crop_box = None
	_original_texture_coords = None
	_scale_x = 1.0
	_scale_y = 1.0

	def _crop(self, x1, y1, x2, y2):
		if self.crop_box != None:
			kl, kb, kr, kt = self.crop_box
			return (
				clamp(x1, kl, kr),
				clamp(y1, kb, kt),
				clamp(x2, kl, kr),
				clamp(y2, kb, kt)
			)
		return (x1, y1, x2, y2)

	def _crop_texture(self, x1, y1, x2, y2):
		if self.crop_box != None:
			if self._original_texture_coords == None:
				if any(self._vertex_list.tex_coords):
					self._original_texture_coords = self._vertex_list.tex_coords[:]
			else:
				l = self._original_texture_coords[0]
				r = self._original_texture_coords[3]
				b = self._original_texture_coords[1]
				t = self._original_texture_coords[7]
				kl, kb, kr, kt = self.crop_box
				tl = mir_lerp(l, r, x1, x2, kl)
				tr = mir_lerp(l, r, x1, x2, kr)
				tb = mir_lerp(b, t, y1, y2, kb)
				tt = mir_lerp(b, t, y1, y2, kt)
				if self._scale_x < 0:
					tl, tr = tr, tl
				if self._scale_y < 0:
					tb, tt = tt, tb
				self._vertex_list.tex_coords[:] = (
					tl, tb, 0.,
					tr, tb, 0.,
					tr, tt, 0.,
					tl, tt, 0.
				)

	def _update_position(self):
		img = self._texture
		if not self._visible:
			vertices = [0, 0, 0, 0, 0, 0, 0, 0]
		elif self._rotation:
			# raise NotImplementedError('Cropped Sprites do not support roation')
			x1 = -img.anchor_x * self._scale_x
			y1 = -img.anchor_y * self._scale_y
			x2 = x1 + img.width * self._scale_x
			y2 = y1 + img.height * self._scale_y
			x = self._x
			y = self._y
			r = -math.radians(self._rotation)
			cr = math.cos(r)
			sr = math.sin(r)
			ax = x1 * cr - y1 * sr + x
			ay = x1 * sr + y1 * cr + y
			bx = x2 * cr - y1 * sr + x
			by = x2 * sr + y1 * cr + y
			cx = x2 * cr - y2 * sr + x
			cy = x2 * sr + y2 * cr + y
			dx = x1 * cr - y2 * sr + x
			dy = x1 * sr + y2 * cr + y
			vertices = [ax, ay, bx, by, cx, cy, dx, dy]
		elif self._scale_x != 1.0 or self._scale_y != 1.0:
			x1 = self._x - img.anchor_x * self._scale_x
			y1 = self._y - img.anchor_y * self._scale_y
			x2 = x1 + img.width * self._scale_x
			y2 = y1 + img.height * self._scale_y
			self._crop_texture(x1, y1, x2, y2)
			x1, y1, x2, y2 = self._crop(x1, y1, x2, y2)
			vertices = [x1, y1, x2, y1, x2, y2, x1, y2]
		else:
			x1 = self._x - img.anchor_x
			y1 = self._y - img.anchor_y
			x2 = x1 + img.width
			y2 = y1 + img.height
			self._crop_texture(x1, y1, x2, y2)
			x1, y1, x2, y2 = self._crop(x1, y1, x2, y2)
			vertices = [x1, y1, x2, y1, x2, y2, x1, y2]
		if not self._subpixel:
			vertices = [int(v) for v in vertices]
		self._vertex_list.vertices[:] = vertices

class AllocatorException(Exception):
	'''The allocator does not have sufficient free space for the requested
	image size.'''
	pass

class _Strip(object):
	def __init__(self, y, max_height):
		self.x = 0
		self.y = y
		self.max_height = max_height
		self.y2 = y

	def add(self, width, height):
		assert width > 0 and height > 0
		assert height <= self.max_height

		x, y = self.x, self.y
		self.x += width
		self.y2 = max(self.y + height, self.y2)
		return x, y

	def compact(self):
		self.max_height = self.y2 - self.y

class Allocator(object):
	def __init__(self, width, height, padding = 0):
		assert width > 0 and height > 0
		self.width = width
		self.height = height
		self.padding = padding
		self.strips = [_Strip(0, height)]
		self.used_area = 0

	def alloc(self, width, height):
		width += self.padding * 2
		height += self.padding * 2
		for strip in self.strips:
			if self.width - strip.x >= width and strip.max_height >= height:
				self.used_area += width * height
				x, y = strip.add(width, height)
				return (x + self.padding, y + self.padding)

		if self.width >= width and self.height - strip.y2 >= height:
			self.used_area += width * height
			strip.compact()
			newstrip = _Strip(strip.y2, self.height - strip.y2)
			self.strips.append(newstrip)
			return newstrip.add(width, height)

		raise AllocatorException('No more space in %r for box %dx%d' % (
				self, width, height))

class TextureAtlas(object):
	def __init__(self, width = 256, height = 256, padding = 0):
		self.texture = pyglet.image.Texture.create(
			width, height, pyglet.gl.GL_RGBA, rectangle=True)
		self.allocator = Allocator(width, height, padding)

	def add(self, img):
		x, y = self.allocator.alloc(img.width, img.height)
		self.texture.blit_into(img, x, y, 0)
		region = self.texture.get_region(x, y, img.width, img.height)
		return region

class TextureBin(object):
	def __init__(self, texture_width = 256, texture_height = 256, padding = 0):
		self.atlases = []
		self.texture_width = texture_width
		self.texture_height = texture_height
		self.padding = padding

	def add(self, img):
		for atlas in list(self.atlases):
			try:
				return atlas.add(img)
			except AllocatorException:
				# Remove atlases that are no longer useful (this is so their
				# textures can later be freed if the images inside them get
				# collected).
				if img.width < 64 and img.height < 64:
					self.atlases.remove(atlas)

		atlas = TextureAtlas(self.texture_width, self.texture_height, self.padding)
		self.atlases.append(atlas)
		return atlas.add(img)

############################################### UTILITIES


BLEND_MODES = {
	None: (770, 771),
	'normal': (770, 771),
	'add': (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE),
	'subtract': (pyglet.gl.GL_DST_COLOR, pyglet.gl.GL_ZERO)
}


############################################### RESOURCE OBJECTS

def lower_power_of_2(x):
	r = 1
	while x > 0:
		x >>= 1
		r <<= 1
	return r >> 1

bin_size = lower_power_of_2(pyglet.gl.GL_MAX_TEXTURE_SIZE)
texture_bin = TextureBin(bin_size, bin_size, 2)

class image:

	__slots__ = ['image', 'is_smooth', 'flip_cache']

	def __init__(self, file_obj = None, texture = None):
		assert(file_obj or texture)
		if file_obj:
			self.image = pyglet.image.load('hint.png', file = file_obj)
			if self.image.width < bin_size // 2 and self.image.height < bin_size // 2:
				self.image = texture_bin.add(self.image)
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

	def get_frame(self, frame):
		return image(texture = self.grid[frame])


class sprite:

	__slots__ = ['sprite']

	def __init__(self, img = None, x = 0, y = 0, batch = None, blend = None):
		# assert(isinstance(batch, fireform.engine.pyglet.batch))
		blend_src, blend_dest = BLEND_MODES.get(blend)
		self.sprite = CroppedSprite(
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

############################################### SOUND

class sound:

	__slots__ = ['media_object']

	def __init__(self, file_object, stream = False):
		self.media_object = pyglet.media.load(
			'file.wav',
			file = file_object,
			streaming = stream
		)

class sound_player:

	__slots__ = ['player']

	def __init__(self, *sounds, volume = 1.0, paused = False):
		self.player = pyglet.media.Player()
		self.volume = volume
		for i in sounds:
			self.player.queue(i.media_object)
		if not paused:
			self.player.play()

	@property
	def volume(self):
		return self.player.volume

	@volume.setter
	def volume(self, value):
		self.player.volume = max(0, min(1, value))

	def play(self):
		self.player.play()

	def pause(self):
		self.player.pause()

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
			color = options.get('color', (0, 0, 0, 255)),
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

def set_clear_colour(colour):
	pyglet.gl.glClearColor(*colour)

def default_draw_handler(world):
	world.handle_message(fireform.message.draw('default'))

def set_blend_mode(mode):
	pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
	pyglet.gl.glBlendFunc(*BLEND_MODES[mode])

def run(the_world, **kwargs):
	"""Create the window and run the game."""

	global w_window_width
	global w_window_height
	global last_draw
	global game_window
	global world

	world = the_world

	w_window_width = kwargs.get('window_width', 1280)
	w_window_height = kwargs.get('window_height', 800)

	# Deprecated feature
	mouse_sensitivity = kwargs.get('mouse_sensitivity', 1)

	config = pyglet.gl.Config(sample_buffers = 1, samples = 0, double_buffer = True)

	fullscreen = kwargs.get('fullscreen', False)
	window_style = pyglet.window.Window.WINDOW_STYLE_DEFAULT

	if kwargs.get('borderless', False):
		window_style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS

	vsync = kwargs.get('vsync', False)

	game_window = pyglet.window.Window(
		width = w_window_width,
		height = w_window_height,
		vsync = vsync,
		config = config,
		resizable = True,
		style = window_style,
		fullscreen = fullscreen
	)

	if 'position' in kwargs:
		x, y = kwargs['position']
		game_window.set_location(x, y)

	# This prevent the on_draw event being triggered every single time anything happens.
	# It also prevents the flipping of the buffer.
	game_window.invalid = True

	set_clear_colour(kwargs.get('clear_colour', (1, 1, 1, 1)))

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

	TARGET_TICKS = kwargs.get('ticks_per_second', 60)
	DRAW_EVERY = kwargs.get('draw_rate', 1)
	INTERVAL = 1 / TARGET_TICKS

	draw_handler = kwargs.get('draw_handler', default_draw_handler)
	fps_display = None

	def update(delta_time):
		# if delta_time > INTERVAL or True:
		# 	print('update(', delta_time, ')')
		world.refresh_entities()
		world.handle_message(fireform.message.mouse_move_raw(mouse_raw_x, mouse_raw_y))
		world.handle_message(fireform.message.mouse_move(*translate_cursor(mouse_raw_x, mouse_raw_y)))
		world.handle_message(fireform.message.tick())
		update.tick_counter += 1
		if update.tick_counter % DRAW_EVERY == 0:
			game_window.clear()
			# world.handle_message(fireform.message.draw())
			draw_handler(world)
			if fps_display:
				fps_display.draw()
			# game_window.flip()

	update.tick_counter = 0

	if kwargs.get('show_fps', True):
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
