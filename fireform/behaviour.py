class base:
	"""Base class for behaviours.

	All behaviours need to inherit from this, otherwise they will not be considered behaviours.
	"""

	def handle_message(self, world, entity, message):
		"""Used internally."""
		func_name = 'm_' + message.decipher_name()
		if hasattr(self, func_name):
			# print('handling', message.decipher_name())
			return getattr(self, func_name)(world, entity, message)

	def can_handle_message(self, name):
		"""Used to check if this behaviour can handle a message."""
		func_name = 'm_' + name
		return hasattr(self, func_name)

	def kill(self):
		setattr(self, '_dead', True)

	def is_dead(self):
		return hasattr(self, '_dead')

	# Weapons of a forgotten era
	def name(self):
		return ''

	def has_name(self):
		if isinstance(self.name, str):
			return True
		return self.name() != ''

	def decipher_name(self):
		if isinstance(self.name, str):
			return self.name
		return self.name()
