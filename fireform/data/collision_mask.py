from fireform.data.base import base


VALID_SHAPES = {'circle', 'rectangle', 'line_up', 'line_down'}


class collision_mask(base):
	""" Specifies the shape of the entity to be used when
		considering collisions.

		:Parameters:
			`shape`: str
				The shape of the mask. Valid values are
				- ``'circle'``
				- ``'rectangle'``
				- ``'line_up'``
				- ``'line_down'``
	"""

	__slots__ = ['_shape']

	name = 'collision_mask'

	def __init__(self, shape = 'circle'):
		self.shape = shape

	@property
	def shape(self):
		return self._shape

	@shape.setter
	def shape(self, value):
		assert(value in VALID_SHAPES)
		self._shape = value
		return value

	def __str__(self):
		return 'mask: {}'.format(self._shape)
