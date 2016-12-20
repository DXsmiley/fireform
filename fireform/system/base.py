class base:
	"""Base class for systems to inherit from."""

	def handle_message(self, world, message):
		func_name = 'm_' + message.decipher_name()
		if hasattr(self, func_name):
			getattr(self, func_name)(world, message)

	def attach(self, world):
		pass
