class base:
	"""Base class for systems to inherit from."""

	def handle_message(self, world, message):
		func_name = 'm_' + message.decipher_name()
		if hasattr(self, func_name):
			f = getattr(self, func_name)
			if not world.frozen or hasattr(f, '_surpass_frozen'):
				f(world, message)

	def attach(self, world):
		pass
