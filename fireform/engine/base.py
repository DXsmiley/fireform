"""

	This file should act as a guideline to anyone wanting to implement
	their own engine. Documentation should also be included here,
	since all engines should have pretty much the same set of features

"""

class image:

	def __init__(self, file_obj = None, texture = None):
		assert(file_obj or texture)

	@property
	def width(self):
		raise NotImplementedError

	@property
	def height(self):
		raise NotImplementedError

	def smooth(self, smooth = None):
		raise NotImplementedError

	# Subject to change
	def get_region(self, x, y, w, h):
		raise NotImplementedError

	@property
	def anchor_x(self):
		raise NotImplementedError

	@anchor_x.setter
	def anchor_x(self, value):
		raise NotImplementedError

	@property
	def anchor_y(self):
		raise NotImplementedError

	@anchor_y.setter
	def anchor_y(self, value):
		raise NotImplementedError

# Move the camera to an absolute position
def camera_apply(centre_x, centre_y, zoom):
	raise NotImplementedError

# Reset the camera to its default position.
def camera_dispel():
	raise NotImplementedError

def run(the_world, **kwargs):
	raise NotImplementedError
