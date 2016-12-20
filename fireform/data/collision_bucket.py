from fireform.data.base import base

class collision_bucket(base):
	""" Specifies the bucket of collisions into which this entity
		should be entered. Entities need to be in the same bucket
		in order to recieve collision events.

		Two entities that are both extroverts cannot collide with each other.
	"""

	name = 'collision_bucket'

	def __init__(self, bucket = 'default', extrovert = False):
		self.bucket = bucket
		self.extrovert = extrovert

	def __str__(self):
		return 'cb: {}'.format(self.bucket)
