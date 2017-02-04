from fireform.data.base import base

class layer(base):
	""" Specifies the layer that the visual aspects of this
		entity should be drawn onto.
	"""

	name = 'layer'
	# attribute_name = 'layer'

	def __init__(self, layer = 'default'):
		self.layer = layer

	def __str__(self):
		return self.layer
