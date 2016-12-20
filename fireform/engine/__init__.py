import sys

current = None

def load(name):
	global current
	print('Loading engine:', name)
	if name == 'pyglet':
		import fireform.engine.pyglet
		current = fireform.engine.pyglet
	elif name == 'sdl2':
		import fireform.engine.sdl2
		current = fireform.engine.sld2
	else:
		raise ValueError('No engine with name ' + name)
