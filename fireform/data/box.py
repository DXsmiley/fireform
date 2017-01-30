# I feel kind of bad for lumping multiple things that were be seperated into
# this one component, but I think it's for the best. This will allow for the
# simplification of a lot of other code.

from fireform.data.base import base
import fireform.geom
import copy

class box(base):
	"""Represents the bounding box of an entity.

	:Attributes:
		`x` : float
			The x ordinate of the box's origin.
		`y` : float
			The y ordinate of the box's origin.
		`width` : float
			The width of the box.
		`height` : float
			The height of the box.
		`anchor_x` : float
			The position of the box's x origin relative to the sides of the box. 0 is on the left, 1 is on the right and 0.5 is in the middle.
			Defaults to 0.5.
		`anchor_y` : float
			The position of the box's y origin relative to the sides of the box. 0 is on the bottom, 1 is on the top and 0.5 is in the middle.
			Defaults to 0.5.

	"""

	__slots__ = ['pos', 'size', 'anchor']

	name = 'box'
	attribute_name = 'box'

	def __init__(self, x = 0, y = 0, pos = None, width = 10, height = 10, size = None, anchor_x = 0.5, anchor_y = 0.5, anchor = None):

		if (pos): x, y = pos
		if (size): width, height = size
		if (anchor): anchor_x, anchor_y = anchor

		self.position = fireform.geom.vector(x, y)
		self.size = fireform.geom.vector(width, height)
		self.anchor = fireform.geom.vector(anchor_x, anchor_y)

	@property
	def x(self):
		return self.position.x

	@x.setter
	def x(self, v):
		self.position.x = v

	@property
	def y(self):
		return self.position.y

	@y.setter
	def y(self, v):
		self.position.y = v

	@property
	def width(self):
		return self.size.x

	@width.setter
	def width(self, v):
		self.size.x = v

	@property
	def height(self):
		return self.size.y

	@height.setter
	def height(self, v):
		self.size.y = v

	@property
	def left(self):
		"""The x co-ordinate of the left hand side of the box.

		Setting this property will change the box's position and keep its width the same.
		"""
		return self.position.x - (self.size.x * self.anchor.x)

	@left.setter
	def left(self, v):
		self.position.x = v + (self.size.x * self.anchor.x)

	@property
	def right(self):
		"""The x co-ordinate of the right hand side of the box.

		Setting this property will change the box's position and keep its width the same.
		"""
		return self.position.x + self.size.x - (self.size.x * self.anchor.x)

	@right.setter
	def right(self, v):
		self.position.x = v - self.size.x + (self.size.x * self.anchor.x)

	@property
	def bottom(self):
		"""The y co-ordinate of the bottom of the box.

		Setting this property will change the box's position and keep its height the same.
		"""
		return self.position.y - (self.size.y * self.anchor.y)

	@bottom.setter
	def bottom(self, v):
		self.position.y = v + (self.size.y * self.anchor.y)

	@property
	def top(self):
		"""The y co-ordinate of the top of the box.

		Setting this property will change the box's position and keep its height the same.
		"""
		return self.position.y + self.size.y - (self.size.y * self.anchor.y)

	@top.setter
	def top(self, v):
		self.position.y = v - self.size.y + (self.size.y * self.anchor.y)

	@property
	def area(self):
		"""The box's area."""
		return self.size.x * self.size.y

	@property
	def rectangle(self):
		"""A :class:`fireform.geom.rectangle` in the same space as the box."""
		return fireform.geom.rectangle(self.left, self.bottom, self.right, self.top)

	def contains(self, point):
		"""Returns true iff the point lies inside the box.

		:Parameters:
			`point` : :class:`fireform.geom.vector`
				The point to test.
		"""
		return self.left < point.x < self.right and self.bottom < point.y < self.top

	def __copy__(self):
		return box(
			pos = copy.copy(self.position),
			size = copy.copy(self.size),
			anchor = copy.copy(self.anchor)
		)

	def __str__(self):
		return "x: {:.2f}, y:{:.2f}, l: {:.2f}, b: {:.2f}, r: {:.2f}, t: {:.2f}".format(
			self.x, self.y, self.left, self.bottom, self.right, self.top
		)
