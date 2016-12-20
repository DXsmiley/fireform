"""

	File contains utility functions for controlling the flow of coroutines, because they're cool.

"""

# Wait for message (should maybe be moved to fireform.utils)

import fireform.behaviour
import fireform.entity

class message_waiter(fireform.behaviour.base):

	name = 'message_waiter'

	def __init__(self, event_name, predicate):
		setattr(self, 'm_' + event_name, self._complete)
		self.predicate = predicate
		self.waiting = True
		self.message = None

	def _complete(self, world, entity, message):
		if self.predicate(message):
			self.waiting = False
			self.message = message


def wait_for_message(world, event_name, check_rate = 1, predicate = lambda : True):
	receiver = fireform.entity.entity(message_waiter(event_name, predicate))
	world.add_entity(receiver)
	while receiver['message_waiter'].waiting:
		yield check_rate
	return receiver['message_waiter'].message
