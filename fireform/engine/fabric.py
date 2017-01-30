from com.fabricjs import fabric

import fireform.message

def default_draw_handler(world):
	world.handle_message(fireform.message.generic('draw'))

def run(the_world, **kwargs):

	canvas = __new__ (fabric.Canvas ('canvas', {'backgroundColor': 'black', 'originX': 'center', 'originY': 'center'}))

	kwargs = {}
	TARGET_TICKS = kwargs.get('ticks_per_second', 60)
	DRAW_EVERY = kwargs.get('draw_rate', 1)
	INTERVAL = 1 / TARGET_TICKS

	draw_handler = kwargs.get('draw_handler', default_draw_handler)
	fps_display = None

	def step():
		the_world.refresh_entities()
		# the_world.handle_message(fireform.message.mouse_move_raw(mouse_raw_x, mouse_raw_y))
		# the_world.handle_message(fireform.message.mouse_move(*translate_cursor(mouse_raw_x, mouse_raw_y)))
		the_world.handle_message(fireform.message.tick())
		step.tick_counter += 1
		if step.tick_counter % DRAW_EVERY == 0:
			# game_window.clear()
			draw_handler(the_world)

	step.tick_counter = 0

	window.setInterval(step, INTERVAL)
