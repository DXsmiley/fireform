__pragma__('opov')

class defaultdict:

	def __init__(self, default):
		self.default = default
		self.dict = {}

	def __getitem__(self, key):
		if key not in self.dict:
			self.dict[key] = self.default()
		return self.dict[key]

	def __setitem__(self, key, value):
		self.dict[key] = value

	def __contains__(self, key):
		return key in self.dict
