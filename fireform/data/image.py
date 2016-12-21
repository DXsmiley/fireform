from fireform.data.base import base
import fireform.geom

class image(base):
	"""Used to show an image!

	:Attirbutes:
		`image` : string
			The name of the image to display.
		`frame` : float
			The frame of the animation to display. This will be rounded down when actually determining which frame to show.
		`roation` : float
			Rotation of the image. Clockwise, in degrees.
		`scale` : :class:`fireform.geom.vector`
			How the image should be stretched.
		`speed` : float
			The number of frames to advance per tick.
		`alpha` : int
			The opacity of the image, in the range of 0 to 255 inclusive. 255 is completely solid, 0 is invisible.
		`blend` : string
			Experimental.
		`scissor` : :class:`fireform.entity.entity`
			Experimental.
	"""

	__slots__ = [
		'image', 'frame', 'rotation', 'depth', 'frame_speed', 'scale',
		'alpha', 'frame_last', 'image_last', 'sprite_object', 'blend',
		'scissor'
	]

	name = 'image'
	attribute_name = 'image'

	def __init__(self, image = None, depth = 0, frame = 0, speed = 0, scale = 1, rotation = 0, blend = None, alpha = 255, scissor = None):
		# public things
		self.image = image
		self.frame = frame
		self.rotation = rotation
		self.depth = depth
		self.frame_speed = speed
		self.scale = fireform.geom.vectorify(scale)
		self.alpha = alpha
		self.frame_last = 0
		self.image_last = None
		self.sprite_object = None
		self.blend = blend # Rare use case.
		self.scissor = scissor # This is probably a rare use case. Maybe move it to a different component?

	def __copy__(self):
		return image(self.image, 0, self.frame, self.frame_speed, self.scale, self.rotation, self.blend, self.alpha)

	# Backwards compatibility shim for the speed property
	@property
	def speed(self):
		return self.frame_speed

	@speed.setter
	def speed(self, value):
		self.frame_speed = value

	def __str__(self):
		return '{} ({:.2f}), rot: {:.2f}, scale: {}'.format(self.image, self.frame, self.rotation, self.scale)
