from copy import copy, deepcopy


class rectangle:

	__slots__ = ['left', 'right', 'bottom', 'top']

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

	def __init__(self, *args):
		if len(args) == 0:
			self.x = self.y = 0
		elif len(args) == 1:
			self.x, self.y = args[0]
		elif len(args) == 2:
			self.x, self.y = args
		else:
			raise ValueError('Too many arguments to construct vector')

	def length(self):
		return (self.x ** 2 + self.y ** 2) ** 0.5

	def magnitude(self):
		return self.length()

	def __add__(self, other):
		return vector(self.x + other.x, self.y + other.y)

	def __iadd__(self, other):
		self.x += other.x
		self.y += other.y
		return self

	def __sub__(self, other):
		return vector(self.x - other.x, self.y - other.y)

	def __isub__(self, other):
		self.x -= other.x
		self.y -= other.y
		return self

	def __mul__(self, other):
		return vector(self.x * other, self.y * other)

	def __imul__(self, other):
		self.x *= other
		self.y *= other
		return self

	def __truediv__(self, other):
		return vector(self.x / other, self.y / other)

	def __itruediv__(self, other):
		self.x /= other
		self.y /= other
		return self

	def __ilshift__(self, other):
		""" Acts as a in-place setter, as the equality operator cannot be overloaded. """
		self.x = other.x
		self.y = other.y
		return self

	def cmul(self, other):
		"""Component-wise multiplication"""
		return vector(self.x * other.x, self.y * other.y)

	def normalised(self, length = 1):
		m = self.length()
		if m == 0:
			return vector(0, 0)
		return vector(self.x / m * length, self.y / m * length)

	@property
	def perpendicular(self):
		""" The vector rotated clockwise 90 degrees """
		return vector(self.y, -self.x)

	@property
	def flipped(self):
		""" The vector inverted """
		return vector(-self.x, -self.y)

	@property
	def line(self):
		""" The vector but every time it's a vector it's actually a line """
		return line((0, 0), self)

	def __copy__(self):
		return vector(self.x, self.y)

	def __iter__(self):
		yield self.x
		yield self.y

	def __str__(self):
		return '<{:.2f}, {:.2f}>'.format(self.x, self.y)


class line:

	def __init__(self, p, r):
		self.p = vectorify(p)
		self.r = vectorify(r)

	def projection_factor(self, s):
		if s == self.p: return 0
		if s == self.r: return 1
		d = self.r - self.p
		return ((s.x - self.p.x) * d.x + (s.y - self.p.y) * d.y) / d.magnitude()

	def project(self, s):
		if s == self.p or self == self.r: return copy(s)
		f = self.projection_factor(s)
		return self.p + (self.r - self.p) * f

	def project_clamped(self, s):
		if s == self.p or self == self.r: return copy(s)
		f = min(max(0, self.projection_factor(s)), 1)
		return self.p + (self.r - self.p) * f

	def __eq__(self, other):
		return isinstance(other, line) and ((self.p == other.p and self.r == other.r) \
			or (self.p == other.r and self.r == other.p))


def distance(v, w):
	return (v - w).magnitude()


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
