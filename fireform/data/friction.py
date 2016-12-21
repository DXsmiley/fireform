from fireform.data.base import base
from fireform.geom import vector

class friction(vector, base):
	"""Multiplies the velocity of an entity every tick, causing it to accelerate or decelerate."""

	name = 'friction'
	attribute_name = 'friction'

	def __init__(self, x = 1, y = 1):
		self.x = x
		self.y = y
