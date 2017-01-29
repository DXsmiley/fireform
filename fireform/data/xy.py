from fireform.data.base import base
from fireform.geom import vector

class xy(vector, base):
	"""Base class for vector-based datum to inherit from."""

	@property
	def vector(self):
		return vector(self.x, self.y)

	@vector.setter
	def vector(self, v):
		self.x = v.x
		self.y = v.y
