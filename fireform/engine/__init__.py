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
		raise Exception('The pyglet engine does not work in the browser')
	elif name == 'sdl2':
		raise Exception('The sdl2 engine does not work in the browser')
	else:
		raise ValueError('No engine with name ' + name)
