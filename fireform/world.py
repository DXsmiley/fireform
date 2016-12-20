import copy
import traceback
import collections
import inspect
import fireform.message
import fireform.efilter
import fireform.util.timer

class world:
	""" World used to control game events and steps.
		Holds a list of entities.
	"""

	def __init__(self):
		"""Creates a new world!"""
		self.entities = []
		self.systems = []
		self.systems_by_name = {}
		l = lambda : collections.defaultdict(list)
		self.message_handlers = l()
		self.message_handlers_by_entity = collections.defaultdict(l)
		self.message_types = set()
		self.filter_root = fireform.efilter.Filter('')

	def refresh_entities(self):
		"""Remove all dead entities from the list, and sort the living ones by ordering.

		Any entities added or destroyed will invalidate the list. You can call this to
		clean it up (but it is somewhat expensive)."""
		dead = [i for i in self.entities if not i.alive]
		self.entities[:] = [i for i in self.entities if i.alive]
		for i in dead:
			if i in self.message_handlers_by_entity:
				del self.message_handlers_by_entity[i]
			self.filter_root.remove(i)
			self.post_message(fireform.message.dead_entity(i))
		self.entities.sort(key = lambda x : x.ordering)

	def add_entity(self, entity):
		"""Add a single entity to the world."""
		assert(isinstance(entity, fireform.entity.entity))
		self.entities.append(entity)
		for t in self.message_types:
			self.register_message_handler(entity, t)
		self.filter_root.insert(entity)
		self.handle_message(fireform.message.new_entity(entity))

	def add_entities(self, entities):
		"""Add multiple entities to the world.

		'entities' should be a list of entity objects."""
		for i in entities:
			self.add_entity(i)

	def destroy_all_entities(self):
		"""Kills all entities in the world.
		This thing is *merciless*."""
		for i in self.entities:
			i.kill()
		self.entities = []

	def add_system(self, system):
		"""Add a system to the world"""
		self.systems.append(system)
		self.systems_by_name[system.name()] = system
		system.attach(self)

	def register_message_handler(self, entity, message_type):
		for behaviour in entity.behaviours_list:
			if behaviour.can_handle_message(message_type):
				self.message_handlers[message_type].append((entity, behaviour))
				self.message_handlers_by_entity[entity][message_type].append(behaviour)

	def register_message_type(self, mtype):
		if mtype not in self.message_types:
			self.message_types.add(mtype)
			for i in self.entities:
				if i.alive:
					self.register_message_handler(i, mtype)

	def handle_message_result(self, result):
		# This feels wrong in so many ways...
		# But the syntactic sugar is too sweet to ignore.
		if inspect.isgenerator(result):
			timer = fireform.util.timer.create_slim(result)
			if timer:
				self.add_entity(timer)

	def handle_message(self, message):
		"""Used internally."""
		# If we encounter an unknown message type, record it
		# and register the handlers on all existing entities
		mtype = message.decipher_name()
		# print('world handling', mtype)
		self.register_message_type(mtype)
		for i in self.systems:
			self.handle_message_result(i.handle_message(self, message))
		self.message_handlers[mtype] = list(filter(lambda e: e[0].alive, self.message_handlers[mtype]))
		for entity, behaviour in self.message_handlers[mtype]:
			self.handle_message_result(behaviour.handle_message(self, entity, message))

		# for i in (i for i in self.entities if i.alive):
			# i.handle_message(self, message)

	def handle_message_private(self, message, entities):
		"""Used internally."""
		mtype = message.decipher_name()
		self.register_message_type(mtype)
		for entity in entities:
			for behaviour in self.message_handlers_by_entity[entity][mtype]:
				self.handle_message_result(behaviour.handle_message(self, entity, message))

	def post_message(self, message):
		"""Sends a message to all systems and entities in the world."""
		self.handle_message(message)

	def post_message_private(self, message, entities):
		"""Sends a message to a few entities and anything that is observing those entities."""
		if isinstance(entities, fireform.entity.entity):
			entities = [entities]
		self.handle_message_private(message, entities)
