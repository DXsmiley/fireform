# Things that I wanted in fireform but didn't need to be hard-coded into the engine.
# This also contains experemental things that might be moved to somewhere else later.

import fireform.behaviour
import fireform.entity
import fireform.geom
import copy
import warnings
import math
import fireform.util.flow

class behaviour_timer(fireform.behaviour.base):

	def __init__(self, events):
		self.time = 0
		self.place = 0
		self.events = sorted(events, key = lambda x: x[0])

	def m_tick(self, world, entity, message):
		while self.place < len(self.events) and self.events[self.place][0] <= self.time:
			self.events[-1][1]()
			self.place += 1
		if self.place == len(self.events):
			# self.end_timer() # Meybe this one will work?
			entity.kill()
		self.time += 1

	def end_timer(self):
		pass
		# entity.kill()
		# self.kill() # 2016-7-18 : This crashed a thing.

	def name(self):
		return 'fireform.util.behaviour_timer'

class behaviour_timer_repeat(behaviour_timer):

	def end_timer(self):
		self.time = 0
		self.place = 0

def make_timer(events):
	"""Returns an entity that triggers a number of functions after different amouts
	of ticks.

	'events' should be a list of integer-function tuples. The events can be in any
	order. (this might change to be more strict). For two events with the same time,
	no guaratees are given as to their order of execution.
	"""
	warnings.warn('Use fireform.util.timer.create instead, please', DeprecationWarning)
	return fireform.entity.entity(behaviour_timer(events))

def make_timer_repeat(events):
	warnings.warn('Use fireform.util.timer.create instead, please', DeprecationWarning)
	return fireform.entity.entity(behaviour_timer_repeat(events))

class behaviour_avoid_solids(fireform.behaviour.base):
	"""Prevent the entity from overlapping from any other 'solid' entities.

	Requires the 'motion' system with 'collision_mode = split'."""

	def __init__(self, stop = True):
		"""Set stop to true to set velocity to 0 on collisions."""
		self.stop = stop

	def m_collision(self, world, entity, message):
		if entity == message.first or entity == message.second:
			other = message.second if entity == message.first else message.first
			if other['solid'] and message.direction != None:
				if message.direction == 'vertical positive':
					entity['position'].y = other['position'].y - entity['size'].y
				if message.direction == 'vertical negitive':
					entity['position'].y = other['position'].y + other['size'].y
				if message.direction == 'horisontal positive':
					entity['position'].x = other['position'].x - entity['size'].x
				if message.direction == 'horisontal negitive':
					entity['position'].x = other['position'].x + other['size'].x
				if self.stop and 'vertical' in message.direction:
					entity['velocity'].y = 0
				if self.stop and 'horisontal' in message.direction:
					entity['velocity'].x = 0

	def name(self):
		return 'behaviour_avoid_solids'

class behaviour_eight_direction_movement(fireform.behaviour.base):

	def __init__(self, speed = 2):
		self.speed = speed
		self.movement_x = 0
		self.movement_y = 0

	def name(self):
		return 'behaviour_eight_direction_movement'

	def m_tick(self, world, entity, message):
		entity['acceleration'].x = self.movement_x * self.speed
		entity['acceleration'].y = self.movement_y * self.speed

	def m_key_press(self, world, entity, message):
		if message.key == fireform.input.key.RIGHT:
			self.movement_x += 1
		if message.key == fireform.input.key.LEFT:
			self.movement_x -= 1
		if message.key == fireform.input.key.UP:
			self.movement_y += 1
		if message.key == fireform.input.key.DOWN:
			self.movement_y -= 1

	def m_key_release(self, world, entity, message):
		if message.key == fireform.input.key.RIGHT:
			self.movement_x -= 1
		if message.key == fireform.input.key.LEFT:
			self.movement_x += 1
		if message.key == fireform.input.key.UP:
			self.movement_y -= 1
		if message.key == fireform.input.key.DOWN:
			self.movement_y += 1

class mock_xy:
	"""Class used to mock xy-based entity datum.

	"""

	def __init__(self, x, y):
		self.x = x
		self.y = y

class behaviour_follow_mouse(fireform.behaviour.base):

	def __init__(self, raw = False):
		self.raw = raw

	def m_mouse_move(self, world, entity, message):
		if not self.raw:
			entity.box.x = message.x
			entity.box.y = message.y

	def m_mouse_move_raw(self, world, entity, message):
		if self.raw:
			entity.box.x = message.x
			entity.box.y = message.y

def make_cursor_entity(image = 'cursor', raw = False):
	return fireform.entity.entity(
		fireform.data.box(),
		behaviour_follow_mouse(raw = raw),
		fireform.data.image(image),
		tags = 'no-debug'
	)

class behaviour_face_cursor(fireform.behaviour.base):

	def __init__(self, speed = 360):
		self.speed = speed
		self.target = 0

	def m_tick(self, world, entity, message):
		if abs(entity['image'].rotation - self.target) <= self.speed:
			entity['image'].rotation = self.target
		elif entity['image'].rotation < self.target:
			entity['image'].rotation += self.speed
		else:
			entity['image'].rotation -= self.speed

	def m_mouse_move(self, world, entity, message):
		vx = message.x - entity.box.x
		vy = message.y - entity.box.y
		self.target = math.degrees(math.atan2(vx, vy))

class behaviour_parallax_background(fireform.behaviour.base):

	def __init__(self, scale = None, centre = None):
		if scale is None: scale = fireform.geom.vector(0.95, 0.95)
		if centre is None: centre = fireform.geom.vector(0, 0)
		self.scale = scale
		self.centre = centre

	def m_camera_moved(self, world, entity, message):
		m = fireform.geom.vector(message.x, message.y)
		entity.box.position = (m - self.centre).cmul(self.scale) + self.centre

def behaviour_follow_camera():
	return behaviour_parallax_background(scale = fireform.geom.vector(1, 1))

class behaviour_follow_entitiy(fireform.behaviour.base):

	def __init__(self, target, offset = None):
		if offset is None: offset = fireform.geom.vector(0, 0)
		self.offset = fireform.geom.vectorify(offset)
		self.target = target

	def m_tick(self, world, entity, message):
		entity.box.position = self.target.box.position + self.offset
