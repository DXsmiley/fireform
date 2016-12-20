class rectangle:

	def __init__(self, *args):
		if len(args) == 2:
			self.left, self.bottom = args[0]
			self.right, self.top = args[1]
		elif len(args) == 4:
			self.left, self.bottom, self.right, self.top = args
		else:
			raise ValueError('Invalid number of arguments for rectangle.__init__')

	@property
	def degenerate(self):
		return self.left >= self.right or self.bottom >= self.top

	def __iter__(self):
		yield self.left
		yield self.bottom
		yield self.right
		yield self.top

	def __str__(self):
		return '({:.2f} {:.2f} {:.2f} {:.2f})'.format(self.left, self.bottom, self.right, self.top)

class vector:

	__slots__ = ['x', 'y']

	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def length(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5

	def magnitude(self):
		return self.length()

	def __add__(self, other):
		return vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return vector(self.x - other.x, self.y - other.y)

	def __truediv__(self, other):
		return vector(self.x / other, self.y / other)

	def cmul(self, other):
		"""Component-wise multiplication"""
		return vector(self.x * other.x, self.y * other.y)

	def normalised(self, length = 1):
		m = self.length()
		if m == 0:
			return vector(0, 0)
		return vector(self.x / m * length, self.y / m * length)

	def __copy__(self):
		return vector(self.x, self.y)

	def __iter__(self):
		yield self.x
		yield self.y

	def __str__(self):
		return '<{:.2f}, {:.2f}>'.format(self.x, self.y)

def vectorify(k):
	if isinstance(k, vector):
		return vector(k.x, k.y)
	if isinstance(k, tuple) or isinstance(k, list):
		x, y = k
		return vector(x, y)
	if isinstance(k, dict):
		return vector(k.get('x', 0), k.get('y', 0))
	if isinstance(k, int) or isinstance(k, float):
		return vector(k, k)
	return vector(k.x, k.y)

def box_overlap(a, b):
	return a.left < b.right and b.left < a.right and a.bottom < b.top and b.bottom < a.top
