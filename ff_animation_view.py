# Used to preview animations.

HELP = """\
Usage:
	python -m ff_animation_view [resource paths] -i [image name] -f [frame rate] -s [scale factor]

resource paths - The paths in which to search for image files.
	These should be the same as the paths passed to `fireform.resource.load`.
frame rate - The number of frames per second.
scale factor - A decimal. Will scale the image up or down.

While the program is running, you can press R to reload the image.\
"""

import fireform
import random
import sys


arguments = sys.argv[1:][::-1]


def next_argument():
	return arguments.pop()


if len(arguments) == 0:

	print(HELP)

else:

	fireform.engine.load('pyglet')

	world = fireform.world.world()

	world.add_system(fireform.system.camera())
	world.add_system(fireform.system.image())


	name = 'image'
	speed = 1
	scale = 1
	paths = []

	while arguments:
		a = next_argument()
		if a == '-i':
			name = next_argument()
		elif a == '-f':
			speed = float(next_argument()) / 60.0
		elif a == '-s':
			scale = float(next_argument())
		else:
			paths.append(a)

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
