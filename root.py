print('Hello, world!')

if False:
	import fireform

import fireform.engine
import fireform.world
import fireform.main
import fireform.system
import fireform.entity
import fireform.data

fireform.engine.load('fabric')

world = fireform.world.world()

world.add_system(fireform.system.motion())

fireform.entity.entity(
	fireform.data.box()
)

fireform.main.run(world)
