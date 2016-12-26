import warnings

class base:
	""" Base class from which other data objects should inherit

		:Attributes:
			`name`: string
				Specifies the name of the component. Should be overridden in the child class.
				This is used when accessing the component as ``my_entity['name']``. Leave unset
				to make this method of access not available.
			`attribute_name`: string
				This is used when accessing the component as ``my_entity.attribute_name``.
				Leave unset to make this method of access not available.
				It is advisiable not to set this except for components that are accessed very
				frequently.
	"""

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
