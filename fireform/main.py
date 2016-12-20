"""

Module used to start the master game loop.

"""

import fireform

def run(*args, **kwargs):
	"""

	:Parameters:
		`the_world` : `fireform.world.world`
			The world to simulate.
		`window_width` : int
			The initial width of the window.
		`window_height` : int
			The initial height of the window.
		`clear_colour` : tuple
			A tuple of four ints representing a colour.
			Used to clear the window after each frame.
		`show_fps` : bool
			Optional. Defaults to False.
		`mouse_sensitivity` : int
			Defaults to 1. Pending Deprecation.

	"""
	fireform.engine.current.run(*args, **kwargs)

def stop():
	"""Stops the main game loop.
	..warning: Not Implemented"""
	raise NotImplementedError()

def swap_world(new_world):
	return fireform.engine.current.swap_world(new_world)
