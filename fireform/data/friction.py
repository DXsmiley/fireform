from fireform.data.xy import xy
from fireform.geom import vector

class friction(xy):
	"""Multiplies the velocity of an entity every tick, causing it to accelerate or decelerate."""

	name = 'friction'
	attribute_name = 'friction'

	def __init__(self, *args):
		if len(args) == 0:
			self.x = self.y = 1
		elif len(args) == 1:
			self.x = self.y = args[0]
		else:
			self.x, self.y = args
