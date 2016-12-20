from fireform.data.base import base

class solid(base):
	"""Denotes that an entity is 'solid' and cannot be passed though.

		This should probably be deprecated in favour of using the tag.
	"""

	def name(self):
		return 'solid'

	def __str__(self):
		return 'solid'
