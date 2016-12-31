import fireform

def test_velocity():
	NUM_TICKS = 10
	VEL_X = 10
	VEL_Y = 20
	world = fireform.world.world()
	world.add_system(fireform.system.motion())
	entity = world.add_entity(fireform.entity(
		fireform.data.box(x = 0, y = 0),
		fireform.data.velocity(x = VEL_X, y = VEL_Y)
	))
	for i in range(NUM_TICKS):
		world.post_message(fireform.message.tick())
	assert entity.box.x == VEL_X * NUM_TICKS
	assert entity.box.y == VEL_Y * NUM_TICKS
