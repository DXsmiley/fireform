from fireform.data.base import base

class camera(base):
	"""Camera data. You can attach this to entities
	and the camera will follow them around.

	If you
	have multiple entities with a camera, the view
	will be positioned at their average location,
	however the view will NOT zoom if they get too
	far aprt.
	"""

	def __init__(self, zoom = 1, weight = 1):
		self.zoom = zoom
		self.weight = weight

	def name(self):
		return 'camera'

	def __str__(self):
		return 'zoom: {}'.format(self.zoom)
