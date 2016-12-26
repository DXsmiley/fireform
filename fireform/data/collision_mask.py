from fireform.data.base import base

class collision_mask(base):
	""" Specifies the shape of the entity to be used when
		considering collisions.

		:Parameters:
			`shape`: str
				The shape of the mask. Valid values are
				- ``'circle'``
				- ``'rectangle'``
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
		assert(value in {'circle', 'rectangle'})
		self._shape = value
		return value

	def __str__(self):
		return 'mask: {}'.format(self._shape)
