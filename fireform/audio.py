import fireform.resource

def play(name, volume = 1, paused = False):
	sound = fireform.resource.audio(name)
	player = fireform.engine.current.sound_player(sound, volume = volume, paused = paused)
	return player
