"""

	This is used to filter large numbers of entities.

	Filters are designed such that each entity needs to be checked only once.
	That is, the valid state of the entity cannot change once it is accepted by
	the filter. The exception to this is if the entity is destroyed.

	Requirements formatting:

		Function:

			The 'requirements' may be a single function, which takes
			in an entity and outputs either True or False.

		String:

			Each line should have a requirement
			Each line shoud start with a '+', meaning 'this is needed'
				or a '-', meaning 'anything that conforms is out'

			Instead of splitting things by lines, they can be split by commas

			Examples:
				'box' (require the box compoenent)
				'-solid' (can't have the solid component)
				'!alive' (must be alive) (WARNING: NOT IMPLEMENTED)
				'!dead' (must be dead) (WARNING: NOT IMPLEMENTED)
				'#player' (must have the tag 'player')
				'-#particle' (can't have the tag 'particle')

"""


import hashlib
import collections


def parse_rule(rule):
	result = True
	# Rule to check if the entity is alive
	if rule == '!alive':
		raise NotImplementedError('!alive rule is not implemented. Filters require that all entities are alive.')
	# Rule to check if the entity is dead
	if rule == '!dead':
		raise NotImplementedError('!dead rule is not implemented. Filters currently reject all dead entities.')
	# No other special rules starting with # exist
	if rule.startswith('!'):
		raise ValueError(rule + ' is not a valid rule')
	# Consider the negitive sign
	# I might move this to before the special rules so they can be negated as well
	if rule.startswith('-'):
		rule = rule[1:]
		result = False
	if rule.startswith('#'):
		tag = rule[1:]
		return lambda entity: result == (tag in entity.tags)
	name = rule
	return lambda entity: result == (entity[name] != None)


def parse_rules(rules):
	if callable(rules):
		return rules
	else:
		rules = rules.replace(' ', '')
		if rules == '':
			return lambda entity: True
		rules = rules.split(',\n')
		rules.sort()
		functions = []
		for i in rules:
			functions.append(parse_rule(i))
		return lambda entity: all(f(entity) for f in functions)


def hash_rules(rules):
	return hashlib.sha224(rules.encode('utf-8')).hexdigest()


class Filter:

	def __init__(self, rules):
		self.rules = rules.replace(' ', '')
		self.entities = set()
		self.children = []
		self.predicate = parse_rules(self.rules)
		self.hash = hash_rules(self.rules)
		self.rejected = False

	def find_duplicate(self, fil):
		for i in self.children:
			if i.hash == fil.hash:
				return i

	def pipe(self, to, ignore_duplicates = False):
		""" Send the results from one filter directly into another.
			If this filter already has an identical child filter,
			this function will return that filter, and that one should
			be used to avoid duplicates.
		"""
		dup = None
		if not ignore_duplicates:
			dup = self.find_duplicate(to)
		if dup != None:
			# print('A filter duplicate was detected. Ensure it\'s handled correctly.')
			to.rejected = True
			return dup
		else:
			self.children.append(to)
			self.cleanup()
			for i in self.entities:
				to.insert(i)
			return to

	def chain(self, rules):
		""" Spawns a chain of filter hanging off this one, and returns the end.
			This is probably the cleanest way to make filters.
		"""
		rules = rules.split('>')
		current = self
		for i in rules:
			current = current.pipe(Filter(i))
		return current

	def insert(self, entity):
		if self.predicate(entity):
			self.entities.add(entity)
			for i in self.children:
				i.insert(entity)
			return True

	def remove(self, entity):
		if entity in self.entities:
			self.entities.remove(entity)
			for i in self.children:
				i.remove(entity)
			return True

	def __len__(self):
		return len(self.entities)

	def cleanup(self):
		to_remove = []
		for i in self.entities:
			if not i.alive:
				to_remove.append(i)
		for i in to_remove:
			self.entities.remove(i)

	def __iter__(self):
		self.cleanup()
		for i in self.entities:
			yield i

	def active(self):
		self.cleanup()
		for i in self.entities:
			if not i.paused:
				yield i

	def __str__(self):
		s = '{} : {}\n'.format(self.rules, len(self))
		for i in self.children:
			for l in str(i).strip('\n').split('\n'):
				s += '    ' + l + '\n'
		return s


class Sorter:

	def __init__(self, func):
		self.contents = collections.defaultdict(set)
		self.func = func
		self.hash = id(func)

	def insert(self, entity):
		key = self.func(entity)
		self.contents[key].add(entity)

	def remove(self, entity):
		key = self.func(entity)
		self.contents[key].discard(entity)

	def __getitem__(self, key):
		self.contents[key] = set(filter(lambda e: e.alive, self.contents[key]))
		return self.contents[key]
