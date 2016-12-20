import fireform

def run(*args, **kwargs):
	fireform.engine.current.run(*args, **kwargs)

def swap_world(new_world):
	fireform.engine.current.swap_world(new_world)
