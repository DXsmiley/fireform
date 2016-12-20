from fireform.data.base import base

class image_batch(base):
	"""Used to display multiple images.

	These need to be set up manually by you."""

	def __init__(self, batch, sprites):
		self.batch = batch
		self.sprite_objects = sprites

	def name(self):
		return 'image_batch'
