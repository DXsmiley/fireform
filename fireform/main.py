"""

Module used to start the master game loop.

"""

import fireform.engine

def run(*args, **kwargs):
	"""

	:Parameters:
		`the_world` : `fireform.world.world`
			The world to simulate.
		`window_width` : int
			The initial width of the window.
			Defaults to 1280.
		`window_height` : int
			The initial height of the window.
			Defaults to 800.
		`fullscreen` : bool
			Wheather the window should be fullscreen.
			Defaults to False.
		`clear_colour` : tuple
			A tuple of four ints representing a colour.
			Used to clear the window after each frame.
			Defaults to white.
		`show_fps` : bool
			Shows the FPS.
			Defaults to True.
		`ticks_per_second` : int
			The number of tick events that occur every second.
			Defaults to 60.
		`draw_rate` : int
			The frequency at which to re-draw the screen.
			A value of ``1`` will redraw it every tick.
			A value of ``2`` will redraw it every second tick.
			etc...
			Defaults to ``1``.
		`borderless` : bool
			Creates a borderless window.
			Defaults to false.
		`position` : tuple of two ints
			Places the window at a particular location on the screen.
			If not specified, the window will be positioned by the
			operating system.
		`vsync` : bool
			Enables vsync.
			Defaults to False.
		`draw_handler` : callable
			Experimental.

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
