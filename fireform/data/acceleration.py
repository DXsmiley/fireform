from fireform.data.base import base
from fireform.geom import vector
from fireform.data.xy import xy
import warnings

class acceleration(xy):
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
