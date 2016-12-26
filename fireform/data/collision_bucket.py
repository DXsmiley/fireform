from fireform.data.base import base

class collision_bucket(base):
	""" Specifies the bucket of collisions into which this entity
		should be entered. Entities need to be in the same bucket
		in order to recieve collision events.

		:Parameters:
			`bucket`: string
				The name of the bucket. Technically this can actually be
				any type that can be hashed in order to be put into a dictionary
			`extrovert`: bool
				Whether the entity is 'extroverted'.
				Two entities that are both extroverted cannot collide with each other.
				Defaults to False.
	"""

	name = 'collision_bucket'

	def __init__(self, bucket = 'default', extrovert = False):
		self.bucket = bucket
		self.extrovert = extrovert

	def __str__(self):
		return 'cb: {}'.format(self.bucket)
