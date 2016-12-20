"""

Chaos

A demonstration game for FireForm.

"""

import fireform

# Load the resources. See resources.json for more details.
fireform.resource.load('./template/resources/')

# Create the world
world = fireform.world.world()
world.add_system(fireform.system.debug())
world.add_system(fireform.system.motion())
world.add_system(fireform.system.image())
world.add_system(fireform.system.camera())

# Behaviour to draw the player to the mouse

class mouse_attraction(fireform.behaviour.base):

	def __init__(self):
		self.mouse_x = 0
		self.mouse_y = 0

	def m_tick(self, world, entity, message):
		pos = entity['position']
		acc = entity['acceleration']
		acc.x = (self.mouse_x - pos.x) / 200
		acc.y = (self.mouse_y - pos.y) / 200

	def m_mouse_move(self, world, entity, message):
		self.mouse_x = message.x
		self.mouse_y = message.y

	def name(self):
		return 'mouse_attraction'

# Spawn the objects

def make_player():
	return fireform.entity.entity(
		fireform.data.position(100, 100),
		fireform.data.velocity(0, 0),
		fireform.data.acceleration(0, 0),
		fireform.data.image('face'),
		fireform.data.size(64, 64),
		mouse_attraction()
	)

def make_focus():
	return fireform.entity.entity(
		fireform.data.position(0, 0),
		fireform.data.camera()
	)

world.add_entity(make_player())
world.add_entity(make_focus())

fireform.main.run(world)
