"""

Handles loading and accessing of engines

:Attributes:
	`current`
		The module of the currently loaded engine.

"""

import sys

current = None

def load(name):
	""" Load an engine.

		This should not be called more than once per program execution.

		:Parameters:
			`name`: string
				The name of the engine.
				Currently, only the ``'pyglet'`` engine is valid.
	"""
	global current
	assert(current == None)
	print('Loading engine:', name)
	if name == 'pyglet':
		import fireform.engine.pyglet
		current = fireform.engine.pyglet
	elif name == 'sdl2':
		import fireform.engine.sdl2
		current = fireform.engine.sld2
	else:
		raise ValueError('No engine with name ' + name)
