from fireform.data.base import base
from fireform.geom import vector
import warnings

class acceleration(base):
	"""Acceleration datum.

	Acceleration is defined as change in velocity per tick.
	This will have no impact on the instance unless it also has
	the velocity and position datum objects.

	:Attributes:
		`x`: int
			Acceleration on the x-axis in pixels per tick per tick.
		`y`: int
			Acceleration on the y-axis in pixels per tick per tick.
	"""

	name = 'acceleration'
	attribute_name = 'acceleration'

	def __init__(self, x = 0, y = 0, friction = None):
		self.x = x
		self.y = y
		if friction:
			warnings.warn("'friction' property in 'acceleration' datum is deprecated", DeprecationWarning)
		else:
			friction = 1
		self.friction = friction
