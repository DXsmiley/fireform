def clamp(val, minimum, maximum):
	"""Utility function that really should be in Python by default"""
	return max(min(val, maximum), minimum)
