# import copy
import fireform.behaviour
import fireform.data
import warnings

class DuplicateComponentException(Exception):
	"""This gets thrown when you try to put multiple copies of a component
	onto a single object."""
	pass

class SharedComponentException(Exception):
	"""Thrown when a single component is put onto multiple Entities."""
	pass

# def indent_lines(lines):
# 	lines = '\n' + lines.strip()
# 	lines = lines.reaplce('\n', '\n    ')
# 	return lines[1:]

class entity:
	"""A game entity.

	This class should not be inherited from (because that's not how things work).

	An entities' attibutes and behaviours are defined by the 'blobs' that they are made from.
	"""

	def __init__(self, *contents, ordering = 0, tags = set()):
		"""

		:Parameters:
			`contents` : list
				Datum and Behaviours that should be attached to this entity.
			`ordering` : int
				The entity's "priority" in the world ordering list.
				A smaller number means it receives messages earlier.
				Defaults to 0.
			`tags` : iterable of strings
				String 'tags' to be associated with the entity.
				Tags can be used to later identify entities.
				Defaults to having no tags.
		"""
		self.contents = {}
		self.datum = {}
		self.behaviours = {}
		self.behaviours_list = []
		self.alive = True
		self.ordering = ordering
		self.tags = set(tags.split(' ')) if type(tags) is str else set(tags)
		for i in contents:
			self.attach(i)

	def __getitem__(self, i):
		return self.contents.get(i, None)

	def __setattr__(self, name, value):
		""" This should only be in here during debugging.
			Released games should not have this for performance reasons.
		"""
		if isinstance(self.__dict__.get(name), fireform.data.base) and self.__dict__.get(name) != value:
			warnings.warn('Assignment to ' + name + ' overrides datum component. Perhaps you meant to use "<<=" instead of "=".', stacklevel = 2)
		self.__dict__[name] = value

	def __contains__(self, i):
		return i in self.contents

	def handle_message(self, world, message):
		# This should probably never be called.
		# The world now handles message dispatching,
		# and does so directly to the behaviours
		raise Exception('This should not have happened')
		keys = [i for i in self.behaviours]
		for i in keys:
			if not isinstance(i, str): # Names are going out of phassion!
				self.behaviours[i].handle_message(world, self, message)

	def attach(self, c):
		"""Add either a data or behaviour object to the entity.

		Data and behaviour objects can only be assigned to one entity.
		An entity cannot have more than one of any type of named data of behaviour.
		Note that is may have multiple instances of anonymous datum or behaviours (future feature).

		Do not use this method once the entity has been added to the world.

		:Parameters:
			`c`: `fireform.data.base` or `fireform.behaviour.base`
				The component to add

		"""
		# Make sure the component is only used once... might move this code into the component.
		if c in self.contents:
			raise DuplicateComponentException()
		if hasattr(c, '_ff__used'):
			raise SharedComponentException()
		c._ff__used = True
		# Register it
		self.contents[c.decipher_name()] = c
		self.contents[type(c)] = c
		if isinstance(c, fireform.data.base):
			if c.has_name():
				self.datum[c.decipher_name()] = c
			if c.decipher_attribute_name():
				if hasattr(self, c.decipher_attribute_name()):
					raise Exception('Attribute name clash occured when adding data: ' + str(c))
				else:
					setattr(self, c.decipher_attribute_name(), c)
			self.datum[type(c)] = c
		elif isinstance(c, fireform.behaviour.base):
			if c.has_name():
				self.behaviours[c.decipher_name()] = c
			self.behaviours[type(c)] = c
			self.behaviours_list.append(c)
		else:
			raise TypeError('Components need to be derived from fireform.data.base or fireform.behaviour.base')

	# def detatch(self, name):
	# 	self.contents[name] = None
	# 	self.datum[name] = None
	# 	self.behaviours[name] = None

	def kill(self):
		"""Destroy the entity.

		The entity will be removed from the world on the next tick,
		so you should still check if it is alive when interacting with it.
		"""
		if self.alive:
			self.alive = False
			for k, v in self.behaviours.items():
				v.kill()

	def __str__(self):
		"""Information on the entity

		Gives a human-readable string representing the data stored
		within the entity.
		"""
		s = 'fireform.entity at {} {}\n'.format(hex(id(self)), '' if self.alive else '(DEAD)')
		s += '    data:\n'
		for i, j in self.datum.items():
			if isinstance(i, str) or not j.has_name():
				s += '        {} : {}\n'.format(i, j)
		s += '    behaviours:\n'
		for i, j in self.behaviours.items():
			if isinstance(i, str) or not j.has_name():
				s += '        {} : {}\n'.format(i, j)
		if self.tags:
			s += '    tags: ' + ', '.join(self.tags) + '\n'
		return s

# Compatibility shim, need to prevent sphinx from recursing into a stack overflow
__pragma__('skip')
if 'sphinx' not in __import__('sys').modules:
	entity.entity = entity
__pragma__('noskip')
