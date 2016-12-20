import collections
import itertools

from fireform.system.base import base
from fireform import message
import fireform.data


PARTITION_SIZE = 128


def check_overlap_y(a, b):
	return a.box.bottom < b.box.top and b.box.bottom <  a.box.top


def update_position_x(entities):
	for i in entities:
		i.box.x += i['velocity'].x


def update_position_y(entities):
	for i in entities:
		i.box.y += i['velocity'].y


def get_bucket(entity):
	if entity['collision_bucket']:
		return entity['collision_bucket'].bucket
	return 'default'


def is_extrovert(entity):
	if entity['collision_bucket']:
		return entity['collision_bucket'].extrovert
	return False


def group_by_bucket(entities):
	result = collections.defaultdict(list)
	for i in entities:
		bucket = get_bucket(i)
		result[bucket].append(i)
	return result.values()


class motion(base):
	"""Makes things move around.

	Can also be set to check for collisions."""

	def __init__(self, collision_mode = 'normal'):
		self.collision_mode = collision_mode
		if self.collision_mode not in ('disabled', 'normal', 'split'):
			raise ValueError('collision_mode must be "disabled", "normal" or "split".')
		self.filter_acceleration = None
		self.filter_velocity = None
		self.filter_collisions = None
		self.filter_friction = None
		self.collisions_late = set()

	def name(self):
		return 'fireform.system.motion'

	def attach(self, world):
		self.filter_acceleration = world.filter_root.chain('velocity > acceleration')
		self.filter_friction = world.filter_root.chain('velocity > friction')
		self.filter_velocity = world.filter_root.chain('box > velocity')
		self.filter_collisions = world.filter_root.chain('box > -#no-collision')

	def m_tick(self, world, m):

		# Acceleration
		for i in self.filter_acceleration:
			vel = i[fireform.data.velocity]
			acl = i[fireform.data.acceleration]
			vel.x += acl.x
			vel.y += acl.y
			vel.x *= acl.friction
			vel.y *= acl.friction

		for i in self.filter_friction:
			i.velocity.x *= i.friction.x
			i.velocity.y *= i.friction.y

		self.collisions_late = set()

		if self.collision_mode == 'disabled':
			update_position_x(self.filter_velocity)
			update_position_y(self.filter_velocity)

		elif self.collision_mode == 'normal':
			update_position_x(self.filter_velocity)
			update_position_y(self.filter_velocity)
			self.check_collisions(world, None)

		elif self.collision_mode == 'split':
			update_position_x(self.filter_velocity)
			self.check_collisions(world, 'horisontal')
			update_position_y(self.filter_velocity)
			self.check_collisions(world, 'vertical')

		for a, b in self.collisions_late:
			world.post_message_private(message.collision_late(a, b), [a])
			world.post_message_private(message.collision_late(b, a), [b])

	def check_collisions(self, world, direction_name):
		comparison_count = 0
		collisions = set()
		region_count = 0
		# active = set()
		for bucket in group_by_bucket(self.filter_collisions):
			events = []
			active = collections.defaultdict(set)
			extrov = collections.defaultdict(set)
			for i in bucket:
				if i.box.right > i.box.left and i.box.top > i.box.bottom:
					events.append((i.box.left, i, 'push'))
					events.append((i.box.right, i, 'pop'))
			# Pushes should always be after pops when things have the same x-ordinate
			events.sort(key = lambda x: x[2] == 'push')
			events.sort(key = lambda x: x[0])
			# print(events)
			for place, entity, action in events:
				partition_bottom = int(entity.box.bottom // PARTITION_SIZE)
				partition_top = int(entity.box.top // PARTITION_SIZE) + 1
				ex = is_extrovert(entity)
				if action == 'pop':
					# Only count these things once
					region_count += partition_top - partition_bottom
					# active.discard(entity)
					if ex:
						for i in range(partition_bottom, partition_top):
							extrov[i].discard(entity)
					else:
						for i in range(partition_bottom, partition_top):
							active[i].discard(entity)
				else:
					for i in range(partition_bottom, partition_top):
						for other in active[i]:
							comparison_count += 1
							if check_overlap_y(entity, other):
								collisions.add((entity, other))
					if not ex:
						for i in range(partition_bottom, partition_top):
							for other in extrov[i]:
								comparison_count += 1
								if check_overlap_y(entity, other):
									collisions.add((entity, other))

					if ex:
						for i in range(partition_bottom, partition_top):
							extrov[i].add(entity)
					else:
						for i in range(partition_bottom, partition_top):
							active[i].add(entity)

		for a, b in collisions:
			world.post_message_private(message.collision(a, b, direction_name), [a])
			world.post_message_private(message.collision(b, a, direction_name), [b])

		self.collisions_late.update(collisions)

		debug_sys = world.systems_by_name.get('fireform.system.debug')
		if debug_sys:
			debug_sys.set_stat('collisions.hits', len(collisions))
			debug_sys.set_stat('collisions.misses', comparison_count - len(collisions))
			debug_sys.set_stat('collisions.queries', region_count)
