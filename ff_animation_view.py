#
# Used to preview animations.
#
# python animation.py [image name] [animation speed] [scale factor]
#

HELP = """\
Usage:
	python animation.py [resource paths] -i [image name] -f [frame rate] -s [scale factor]
"""

import fireform
import random
import sys

fireform.engine.load('pyglet')

world = fireform.world.world()

world.add_system(fireform.system.camera())
world.add_system(fireform.system.image())

# print(sys.argv)

if len(sys.argv) == 1:
	print(HELP)
else:

	name = 'image'
	speed = 1
	scale = 1
	paths = []

	i = 1
	while i < len(sys.argv):
		a = sys.argv[i]
		if a == '-i':
			i += 1
			name = sys.argv[i]
		elif a == '-f':
			i += 1
			speed = float(sys.argv[i])
		elif a == '-s':
			i += 1
			scale = float(sys.argv[i])
		else:
			paths.append(a)
		i += 1

	fireform.resource.load(*paths, smooth_images = False)

	class key_commands(fireform.behaviour.base):

		def m_key_press(self, world, entity, message):
			if message.key == fireform.input.key.R:
				fireform.resource.unload()
				fireform.resource.load(*paths, smooth_images = False)

	world.add_entity(fireform.entity.entity(
		fireform.data.box(80, 80),
		fireform.data.image(name, speed = speed, scale = scale),
		fireform.data.camera(),
		key_commands()
	))

	fireform.main.run(world, window_width = 256, window_height = 256)
