"""

A simple demonstration game for FireForm.

"""

import fireform

fireform.engine.load('pyglet')

# Load the resources. See resources.json for more details.
fireform.resource.load('./template/resources/')

# Create the world
world = fireform.world.world()
world.add_system(fireform.system.motion())
world.add_system(fireform.system.camera())
world.add_system(fireform.system.image())
world.add_system(fireform.system.debug())

# Behaviour to draw the player to the mouse

class mouse_attraction(fireform.behaviour.base):

	def __init__(self):
		self.mouse_x = 0
		self.mouse_y = 0

	def m_tick(self, world, entity, message):
		pos = entity['box'].position
		acc = entity['acceleration']
		acc.x = (self.mouse_x - pos.x) / 200
		acc.y = (self.mouse_y - pos.y) / 200

	def m_mouse_move(self, world, entity, message):
		self.mouse_x = message.x
		self.mouse_y = message.y

# Spawn the objects

def make_player():
	return fireform.entity.entity(
		fireform.data.box(x = 100, y = 100, width = 64, height = 64),
		fireform.data.velocity(0, 0),
		fireform.data.acceleration(0, 0),
		fireform.data.image('face'),
		mouse_attraction()
	)

def make_focus():
	return fireform.entity.entity(
		fireform.data.box(0, 0),
		fireform.data.camera()
	)

world.add_entity(make_player())
world.add_entity(make_focus())

fireform.main.run(world)
