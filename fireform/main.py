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
		`ticks_per_second` : int
			The number of tick events that occur every second.
		`draw_rate` : int
			The frequency at which to re-draw the screen.
			A value of ``1`` will redraw it every tick.
			A value of ``2`` will redraw it every second tick.
			Defaults to ``1``.

	"""
	fireform.engine.current.run(*args, **kwargs)

def stop():
	"""
	Stops the main game loop.

	.. warning::
		Not Implemented

	"""
	raise NotImplementedError()

def swap_world(new_world):
	return fireform.engine.current.swap_world(new_world)
