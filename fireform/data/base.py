import warnings

class base:
	"""Base class from which other data objects
	should inherit"""

	# def __init__(self):
	# 	"""Override this, m9."""
	# 	pass

	name = None
	attribute_name = None

	# Names definitely *ARE* things!
	def decipher_name(self):
		if callable(self.name):
			n = self.name()
			warnings.warn('Datum object "{}" is using a function to implement it\'s name'.format(n), DeprecationWarning)
			return n
		else:
			return self.name

	def decipher_attribute_name(self):
		if callable(self.attribute_name):
			n = self.attribute_name()
			warnings.warn('Datum object "{}" is using a function to implement it\'s attribute name'.format(n), DeprecationWarning)
			return n
		else:
			return self.attribute_name

	def has_name(self):
		warnings.warn('Datum object\'s method has_name is deprecated.', DeprecationWarning)
		return self.decipher_name() != None
