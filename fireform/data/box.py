# I feel kind of bad for lumping multiple things that were be seperated into
# this one component, but I think it's for the best. This will allow for the
# simplification of a lot of other code.

from fireform.data.base import base
import fireform.util
import fireform.geom
import copy

class box(base):

	__slots__ = ['pos', 'size', 'anchor']

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
		return self.position.x - (self.size.x * self.anchor.x)

	@left.setter
	def left(self, v):
		self.position.x = v + (self.size.x * self.anchor.x)

	@property
	def right(self):
		return self.position.x + self.size.x - (self.size.x * self.anchor.x)

	@right.setter
	def right(self, v):
		self.position.x = v - self.size.x + (self.size.x * self.anchor.x)

	@property
	def bottom(self):
		return self.position.y - (self.size.y * self.anchor.y)

	@bottom.setter
	def bottom(self, v):
		self.position.y = v + (self.size.y * self.anchor.y)

	@property
	def top(self):
		return self.position.y + self.size.y - (self.size.y * self.anchor.y)

	@top.setter
	def top(self, v):
		self.position.y = v - self.size.y + (self.size.y * self.anchor.y)

	@property
	def area(self):
		return self.size.x * self.size.y

	@property
	def rectangle(self):
		return fireform.geom.rectangle(self.left, self.bottom, self.right, self.top)

	def contains(self, point):
		return self.left < point.x < self.right and self.bottom < point.y < self.top

	def name(self):
		return 'box'

	def attribute_name(self):
		return 'box'

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
