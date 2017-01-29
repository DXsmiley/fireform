import fireform
import math
import random

fireform.engine.load('pyglet')

# Load the resources. See resources.json for more details.

fireform.resource.load('./example/resources/')

# Create the world

world = fireform.world.world()
world.add_system(fireform.system.motion(collision_mode = 'split')) # Moves things
world.add_system(fireform.system.camera()) # Needed to view the world
world.add_system(fireform.system.image())  # Needed to draw images
world.add_system(fireform.system.debug(allow_edit = True, text_colour = (255, 255, 255, 255)))  # Debug info

# This will destroy any objects that leave the boundary of the game.
# This is so that the world doesn't fill up with bullets and start lagging.
class destroy_outside_things(fireform.system.base):

	def __init__(self, limit = 5000):
		self.limit = limit

	def attach(self, world):
		self.filter = world.filter_root.chain('box')

	def name(self):
		return 'destroy_outside_things'

	def m_tick(self, world, message):
		for i in self.filter:
			x = i.box.x
			y = i.box.y
			if x < -self.limit or x > self.limit or y < -self.limit or y > self.limit:
				i.kill()

world.add_system(destroy_outside_things())

# Entities with this behaviour will gradually fade out.
# Once they are no longer visible they will be destroyed.
class behaviour_fade_away(fireform.behaviour.base):

	def __init__(self, steps):
		self.rate = 256 / steps

	def m_tick(self, world, entity, message):
		entity['image'].alpha -= self.rate
		if entity['image'].alpha <= 0:
			entity.kill()

class behaviour_player(fireform.behaviour.base):

	def __init__(self):
		self.target = {'x': 0, 'y': 0} # TODO: Replace this with a vector.
		self.cooldown = 0
		self.shooting = False

	def m_tick(self, world, entity, message):
		self.cooldown -= 1
		if self.shooting and self.cooldown <= 0:
			self.cooldown = 3
			world.add_entity(make_bullet(
				entity.box.x,
				entity.box.y,
				self.target['x'],
				self.target['y']
			))
			fireform.audio.play('shoot', volume = 0.4)

	def m_mouse_move(self, world, entity, message):
		self.target['x'] = message.x
		self.target['y'] = message.y

	def m_mouse_click(self, world, entity, message):
		if message.button == fireform.input.mouse.LEFT:
			self.shooting = True
			self.target['x'] = message.x
			self.target['y'] = message.y

	def m_mouse_release(self, world, entity, message):
		if message.button == fireform.input.mouse.LEFT:
			self.shooting = False

class behaviour_monster(fireform.behaviour.base):

	def __init__(self):
		self.health = 8

	def m_collision(self, world, entity, message):
		other = message.other
		# print(entity, other)
		if 'bullet' in other.tags:
			other.kill()
			world.add_entities(make_particle_burst(other.box.x, other.box.y))
			self.health -= 1
			force = fireform.geom.vector(*other.velocity).normalised(6)
			entity.velocity.x += force.x
			entity.velocity.y += force.y
			fireform.audio.play('hit')
		if self.health == 0:
			entity.kill()

class behaviour_collide_with_solids(fireform.behaviour.base):

	def m_collision(self, world, entity, message):
		if entity in message:
			other = message.other
			if 'solid' in other.tags:
				if message.direction == 'horisontal':
					if entity.velocity.x > 0:
						entity.box.right = other.box.left
					if entity.velocity.x < 0:
						entity.box.left = other.box.right
					entity.velocity.x = 0
				if message.direction == 'vertical':
					if entity.velocity.y > 0:
						entity.box.top = other.box.bottom
					if entity.velocity.y < 0:
						entity.box.bottom = other.box.top
					entity.velocity.y = 0

class behaviour_bounce_on_solids(fireform.behaviour.base):

	def m_collision(self, world, entity, message):
		other = message.other
		if 'solid' in other.tags:
			if message.direction == 'horisontal':
				if entity.velocity.x > 0:
					entity.box.right = other.box.left
				if entity.velocity.x < 0:
					entity.box.left = other.box.right
				entity.velocity.x *= -1
			if message.direction == 'vertical':
				if entity.velocity.y > 0:
					entity.box.top = other.box.bottom
				if entity.velocity.y < 0:
					entity.box.bottom = other.box.top
				entity.velocity.y *= -1

class behaviour_dispel_moveables(fireform.behaviour.base):

	def m_collision_late(self, world, entity, message):
		if 'moveable' in message.other.tags:
			force = entity.box.position - message.other.box.position
			force = force.normalised(3)
			entity.velocity.x += force.x + random.uniform(-1, 1)
			entity.velocity.y += force.y + random.uniform(-1, 1)

def make_player():
	return fireform.entity.entity(
		fireform.data.box(size = (60, 60)),
		fireform.data.camera(weight = 6),
		fireform.data.velocity(),
		fireform.data.acceleration(friction = 0.94),
		fireform.data.image('ship'),
		fireform.data.collision_mask('circle'),
		fireform.util.behaviour_eight_direction_movement(speed = 1),
		fireform.util.behaviour_face_cursor(speed = 30),
		behaviour_player(),
		behaviour_collide_with_solids(),
		behaviour_dispel_moveables(),
		ordering = 10,
		tags = 'player moveable'
	)

def make_bullet(x, y, x_to, y_to):
	return fireform.entity.entity(
		fireform.data.box(
			pos = (x, y),
			size = (12, 12)
		),
		fireform.data.collision_mask('circle'),
		fireform.data.velocity(
			fireform.geom.vector(
				x_to - x + random.randint(-10, 10),
				y_to - y + random.randint(-10, 10)
			).normalised(80)
		),
		fireform.data.image('bullet', blend = 'add', rotation = math.degrees(math.atan2(x_to - x, y_to - y))),
		tags = 'bullet'
	)

def make_monster(x, y):
	return fireform.entity.entity(
		fireform.data.box(
			pos = (x, y),
			size = (80, 80)
		),
		fireform.data.image(
			'monster_cross',
			blend = 'add'
		),
		fireform.data.velocity(),
		fireform.data.acceleration(friction = 0.94),
		behaviour_monster(),
		behaviour_bounce_on_solids(),
		behaviour_dispel_moveables(),
		tags = 'monster moveable'
	)

def make_cursor():
	return fireform.entity.entity(
		fireform.data.box(size = (0, 0)),
		fireform.data.camera(),
		fireform.util.behaviour_follow_mouse(),
		tags = 'no-debug no-collision'
	)

def make_static_image(image, x, y, ordering, blend = None):
	return fireform.entity.entity(
		fireform.data.box(
			pos = (x, y),
			size = fireform.resource.image_size(image)
		),
		fireform.data.image(image, blend = blend),
		ordering = ordering,
		tags = 'no-debug no-collision'
	)

def make_parallax_background(image, x_scale = 0.9, y_scale = 0.9, ordering = -1000, blend = None):
	return fireform.entity.entity(
		fireform.data.box(size = fireform.resource.image_size(image)),
		fireform.data.image(image, blend = blend),
		fireform.util.behaviour_parallax_background(scale = fireform.geom.vector(x_scale, y_scale)),
		ordering = ordering,
		tags = 'no-debug no-collision'
	)

def make_wall(x1, y1, x2, y2):
	return fireform.entity.entity(
		fireform.data.box(
			anchor = (0, 0),
			pos = (x1, y1),
			size = (x2 - x1, y2 - y1)
		),
		fireform.data.solid(),
		tags = 'solid'
	)

def make_boundary(x1, y1, x2, y2):
	return [
		make_wall(x1 - 100, y1, x1, y2),
		make_wall(x2, y1, x2 + 100, y2),
		make_wall(x1, y1 - 100, x2, y1),
		make_wall(x1, y2, x2, y2 + 100)
	]

def make_particle(x, y):
	return fireform.entity.entity(
		fireform.data.box(x, y),
		fireform.data.image('pink_particle', blend = 'add'),
		fireform.data.velocity(random.uniform(-1, 1), random.uniform(-1, 1)).scale_to(random.randint(20, 40)),
		behaviour_fade_away(random.uniform(5, 20)),
		tags = ('no-collision', 'no-debug')
	)

def make_particle_burst(x, y):
	for i in range(10):
		yield fireform.entity.entity(
			fireform.data.box(x, y),
			fireform.data.image('pink_particle', blend = 'add'),
			fireform.data.velocity(
				fireform.geom.vector(
					random.uniform(-1, 1),
					random.uniform(-1, 1)
				).normalised(random.randint(20, 40)),
			),
			behaviour_fade_away(random.uniform(5, 20)),
			tags = ('no-collision', 'no-debug')
		)

world.add_entity(make_player())
world.add_entity(make_cursor())
world.add_entity(make_parallax_background('space_background', x_scale = 0.96, y_scale = 0.96, ordering = -1000))
world.add_entity(make_parallax_background('stars', ordering = -900, blend = 'add'))
world.add_entity(make_static_image('border', 0, 0, -100, blend = 'add'))
world.add_entities(make_boundary(-1500, -1000, 1500, 1000))

for i in range(100):
	world.add_entity(make_monster(
		random.randint(-1000, 1000),
		random.randint(-1000, 1000)
	))

# Run the game

fireform.main.run(world)
