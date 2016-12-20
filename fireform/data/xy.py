from fireform.data.base import base

class xy(base):
	"""Base class for vector-based datum to inherit from."""

	__slots__ = ['x', 'y']

	def __init__(self, x = None, y = None):
		if x != None and y != None:
			self.x = x
			self.y = y
		elif x == None and y == None:
			self.x = 0
			self.y = 0
		else:
			t = x or y
			self.x = t
			self.y = t

	def magnitude(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5

	def scale_to(self, length):
		m = self.magnitude()
		self.x *= length / m
		self.y *= length / m
		return self

	def __iter__(self):
		return iter((self.x, self.y))

	# def get_tuple(self):
		# return (self.x, self.y)

	def __getitem__(self, index):
		if index == 'x':
			return self.x
		elif index == 'y':
			return self.y
		else:
			raise IndexError('fireform.data.xy has no key ' + str(index))

	def __setitem__(self, index, value):
		if index == 'x':
			self.x = value
		elif index == 'y':
			self.y = value
		else:
			raise IndexError('fireform.data.xy has no key ' + str(index))

	def __str__(self):
		return 'xy({:.2f}, {:.2f})'.format(self.x, self.y)
