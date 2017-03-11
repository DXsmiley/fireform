"""

	All inbuilt messages.

"""

import warnings


def surpass_frozen(function):
	""" Decorator to apply to a message handler if it should be called even if the world is frozen. """
	function._surpass_frozen = True
	return function


class base():
	""" Base message from which all other messages need to inherit.

		:Attributes:
			`name` : string
				The name of the message. Behaviour and systems that want to listen for a message
				have to implement a function called ``m_name``. For example, if the message's name
				was ``tick``, the behaviour would have to implement ``m_tick``.

	"""

	# This should be overridden by any class that inherits from this.
	name = lambda self: self.__class__.__name__

	# def name(self):
	# 	"""Returns the name of the message.
	#
	# 	This also identities the function called in the behaviours and system.
	# 	For example if the name is 'lemon_exploded', then the curresponding
	# 	function will be 'm_lemon_exploded'."""
	# 	raise NotImplementedError('A message failed to specify a name')

	def decipher_name(self):
		""" Returns the name of the message.

			This should be used instead of ``name``, since some older messages may use a function to
			implement their name.
		"""
		if isinstance(self.name, str):
			return self.name
		else:
			n = self.name()
			warnings.warn('Message type "{}" is using a function to implement its name'.format(n), DeprecationWarning)
			return n


class generic(base):
	""" Generic messages which hold no data.

		:Attributes:
			`name` : string
				Name of the message.
	"""

	def __init__(self, my_name):
		self.name = my_name


def tick():
	"""This message is dispatched once per game tick."""
	return generic('tick')


def frozen_tick():
	"""This message is dispatched once per tick while the system is paused."""
	return generic('tick')


def animate():
	""" Dispatches once per game tick, after the tick events and before the drae event.
		It exists to seperate the tick-dependent graphics logic from the tick-independent logic.
	"""
	return generic('animate')


class draw(base):
	"""Dispatched whenever a layer is drawn."""

	name = 'draw'

	def __init__(self, layer):
		self.layer = layer


class key_press(base):
	""" Signifies that a key was pressed.

		:Attributes:
			`key` : `fireform.input.key`
				The key that was pressed.
			`modifiers` : something
				The modifier keys (shift, control, etc.) That were
				being held when the key was pressed.
	"""

	name = 'key_press'

	def __init__(self, key, modifiers):
		self.key = key
		self.modifiers = modifiers


class key_release(base):
	""" Signifies that a key was released.

		:Attributes:
			`key` : `fireform.input.key`
				The key that was released.
			`modifiers` : something
				The modifier keys (shift, control, etc.) That were
				being held when the key was released.

	"""

	name = 'key_release'

	def __init__(self, key, modifiers):
		self.key = key
		self.modifiers = modifiers


class new_entity(base):
	""" Signifies that an entitiy was added to the world.

		:Attributes:
			`entity` : :class:`fireform.entity.entity`
				The entity that was just added to the world.

	"""

	name = 'new_entity'

	def __init__(self, entity):
		self.entity = entity


class dead_entity(base):
	"""Signals that an entitity has been killed.

		This is triggered when the world decides to remove it,
		not when entity.kill() is called.

		:Attributes:
			`entity` : :class:`fireform.entity.entity`
				The dead entity.

	"""

	name = 'dead_entity'

	def __init__(self, entity):
		self.entity = entity


class mouse_move(base):
	""" Signifies that the mouse was moved.

		This may not trigger if the mouse is moved
		outside the window.

		:Attributes:
			`x` : float
				The x position of the cursor, within the world.
			`y` : float
				The y position of the cursor, within the world.

	"""

	name = 'mouse_move'

	def __init__(self, x, y):
		self.x = x
		self.y = y

class mouse_release(base):
	""" Signifies the a mouse button was released.

		:Attributes:
			`x` : float
				The x position of the cursor, within the world.
			`y` : float
				The y position of the cursor, within the world.
			`button` : something
				The button that was released.

	"""

	name = 'mouse_release'

	def __init__(self, x, y, button):
		self.x = x
		self.y = y
		self.button = button


class mouse_click(base):
	""" Signifies the a mouse button was clicked.

		:Attributes:
			`x` : float
				The x position of the cursor, within the world.
			`y` : float
				The y position of the cursor, within the world.
			`button` : something
				The button that was pressed.

	"""

	name = 'mouse_click'

	def __init__(self, x, y, button):
		self.x = x
		self.y = y
		self.button = button


class mouse_move_raw(base):
	""" Signifies that the mouse was moved.

		This may not trigger if the mouse is moved
		outside the window.

		:Attributes:
			`x` : float
				The x position of the cursor, relative to the corner of the window.
			`y` : float
				The y position of the cursor, relative to the corner of the window.

	"""

	name = 'mouse_move_raw'

	def __init__(self, x, y):
		self.x = x
		self.y = y


class mouse_click_raw(base):
	""" Signifies the a mouse button was clicked.

		:Attributes:
			`x` : float
				The x position of the cursor, relative to the corner of the window.
			`y` : float
				The y position of the cursor, relative to the corner of the window.
			`button` : something
				The button that was pressed.

	"""

	name = 'mouse_click_raw'

	def __init__(self, x, y, button):
		self.x = x
		self.y = y
		self.button = button


class mouse_release_raw(base):
	""" Signifies the a mouse button was released.

		:Attributes:
			`x` : float
				The x position of the cursor, relative to the corner of the window.
			`y` : float
				The y position of the cursor, relative to the corner of the window.
			`button` : something
				The button that was released.

	"""

	name = 'mouse_release_raw'

	def __init__(self, x, y, button):
		self.x = x
		self.y = y
		self.button = button


class window_resized(base):
	""" Signifies that the window was resized.

		:Attributes:
			`width` : int
				The width of the window.
			`height` : int
				The height of the window.

	"""

	name = 'window_resized'

	def __init__(self, width, height):
		self.width = width
		self.height = height


class collision(base):
	""" Signals that two entities have overlapped.

		fireform.system.motion will send these once per tick until they
		stop colliding.

		This is sent as a private message, so only the entities that actually
		collide will receive it.

		:Attributes:
			`other` : :class:`fireform.entity.entity`
				The *other* entity.
			`direction` : string
				The direction in which the entities were moving when they collided.
				This is only applicable when :class:`the collision mode is set to split<fireform.system.motion>`.
	"""

	name = 'collision'

	def __init__(self, first, second, direction):
		self.first = first
		self.second = second
		self.other = second # <== You see this? It's the future.
		self.direction = direction

	def __contains__(self, item):
		return self.first == item or self.second == item


class collision_late(base):
	""" Signals that two entities have overlapped.

		This event is fired after the main round of collision events, after all objects have finished moving.
		If a collision event is fired, a collision_late event will be fired.

		Collision late events are usefull for when the velocity of an object needs to be changed, because
		that could otherwise mess with some physics logic that relies on knowing the direction that
		the object is moving in.

	"""

	name = 'collision_late'

	def __init__(self, first, second):
		self.first = first
		self.second = second
		self.other = second # <== You see this? It's the future.

	def __contains__(self, item):
		return self.first == item or self.second == item


class collision_enter(base):
	""" Signals that two entities have overlapped.

		This is sent as a private message, so only the entities that actually
		collide will receive it.

		:Attributes:
			`other` : :class:`fireform.entity.entity`
				The *other* entity.
	"""

	name = 'collision_enter'

	def __init__(self, other):
		self.other = other

	def __contains__(self, item):
		return self.first == item or self.second == item


class collision_exit(base):
	""" Signals that two entities have stopped overlapping.

		This is sent as a private message, so only the entities that actually
		collide will receive it.

		:Attributes:
			`other` : :class:`fireform.entity.entity`
				The *other* entity.
	"""

	name = 'collision_exit'

	def __init__(self, other):
		self.other = other

	def __contains__(self, item):
		return self.first == item or self.second == item


class update_tracked_value(base):

	name = 'update_tracked_value'

	def __init__(self, key, value):
		self.key = key
		self.value = value


# I might include these two things in the future.
# I'm not sure what str(key) produces, so I'm leaving them out for now.

# class key_press_targeted(base):

# 	def __init__(self, key, modifiers):
# 		self.key = key
# 		self.modifiers = modifiers

# 	def name(self):
# 		return 'key_press_' + str(self.key)

# class key_release_targeted(base):

# 	def __init__(self, key, modifiers):
# 		self.key = key
# 		self.modifiers = modifiers

# 	def name(self):
# 		return 'key_release_' + str(self.key)
