import collections
import inspect


subscription_cache = {}


def get_message_handles(behaviour):
	global subscription_cache
	the_class = behaviour.__class__
	if the_class not in subscription_cache:
		result = []
		for name, func in inspect.getmembers(the_class):
			if name.startswith('m_'):
				result.append(name[2:])
		subscription_cache[the_class] = result
	return subscription_cache[the_class]


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

	def listening_for(self):
		print(self.__dict__)

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
