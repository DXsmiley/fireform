import json
import warnings
import fireform

cache = {} # Contains images
audio_cache = {} # Contains audio
search_paths = []
do_smooth_images = False

def open_data(filename, mode = 'r'):
	""" Opens a file found in the search paths.

		:Parameters:
			`filename` : str
				The filename.
			`mode` : str
				The mode to open the file in.
				This is the same as the ``mode`` parameter on the builtin ``open`` function.
				Defaults to ``'r'`` (read, text mode).

	"""
	for i in search_paths:
		try:
			f = open(i + filename, mode)
			return f
		except FileNotFoundError:
			pass
	e = 'fireform could not locate {} in paths {}'.format(filename, search_paths)
	raise FileNotFoundError(e)

def open_get_filename(filename, mode = 'rb'):
	# """ Returns the full path of a file in fileform's resource search space.
	#
	# 	:Parameters:
	# 		`filename` : str
	# 			The filename.
	# 		`mode` : str
	# 			The mode to open the file in, since this works by trying to open a lot of different files.
	# 			In practice this shouldn't be changed.
	# 			This is the same as the ``mode`` parameter on the builtin ``open`` function.
	# 			Defaults to ``'rb'``.
	#
	# """
	for i in search_paths:
		try:
			f = open(i + filename, mode)
			f.close()
			return i + filename
		except FileNotFoundError:
			pass
	e = 'fireform could not locate {} in paths {}'.format(filename, search_paths)
	raise FileNotFoundError(e)

def process_anchor(value, size):
	if type(value) is str:
		if value[-1] == '%':
			return int(float(value[:-1]) * size / 100)
	return int(value)

def load(*paths, smooth_images = False):
	""" Load resources.

		:Parameters:
			`paths` : str
				File paths to search relative to the working directory of the game.

				.. note:: This may be changed to be relative to the program directory of the game in the future.

			`smooth_images` : bool
				Set to ``True`` to smooth images when they are resized.
				Most games should enable this. Pixel art games should not.
				Defaults to false.

	"""

	global do_smooth_images
	global cache
	global search_paths

	do_smooth_images = smooth_images

	assert(len(paths) > 0)

	search_paths = [(i + '/').replace('//', '/') for i in paths]

	try:

		with open_data('resources.json') as f:
			resources_json = json.loads(f.read())

	except FileNotFoundError:

		print('No resources.json file found')

	else:

		for name, data in resources_json.get('sheets', {}).items():
			# image = ENGINE.image.load('hint.png', file = open_data(name + '.png', 'rb'))
			with open_data(name + '.png', 'rb') as file_object:
				image = fireform.engine.current.image(file_object)
				# image_grid = ENGINE.image.ImageGrid(image, data.get('y_tiles', 1), data.get('x_tiles', 1))
				image_grid = fireform.engine.current.image_grid(image, data.get('x_tiles', 1), data.get('y_tiles', 1))
				data['smooth'] = data.get('smooth', smooth_images)
				for strip_name, strip_range in data['strips'].items():
					if isinstance(strip_range, int):
						a = strip_range
						b = a + 1
					else:
						a, b = strip_range
					cache[strip_name] = image_grid.get_strip(a, b)
					for i in cache[strip_name]:
						set_image_properties(i, data)

		for name_string, data in resources_json.get('images', {}).items():
			for name in [i.strip() for i in name_string.split(', ')]:
				# i_obj = ENGINE.image.load('hint.png', file = open_data(name + '.png', 'rb'))
				with open_data(name + '.png', 'rb') as file_object:
					i_obj = fireform.engine.current.image(file_object)
					data['smooth'] = data.get('smooth', smooth_images)
					set_image_properties(i_obj, data)
					cache[name] = [i_obj]

		for name, data in resources_json.get('audio', {}).items():
			audio(name, data)


def set_image_properties(image, data):
	image.smooth(data.get('smooth'))
	image.anchor_x = process_anchor(data.get('x_offset', '50%'), image.width)
	image.anchor_y = image.height - process_anchor(data.get('y_offset', '50%'), image.height)


def image(name, frame = 0):
	if name not in cache:
		warnings.warn('Image "{}" not in cache. Being loaded.'.format(name))
		image = fireform.engine.current.image(open_data(name + '.png', 'rb'))
		# image.smooth(smooth_images)
		cache[name] = [image]
	l = len(cache[name])
	return cache[name][frame % l]


def image_size(name):
	i = image(name)
	return i.width, i.height


def audio(name, data = {}):
	raise NotImplementedError('Audio data cannot be loaded at the moment')
	if name not in audio_cache:
		filename = data.get('filename', name + '.wav')
		audio_cache[name] = ENGINE.resource.media(
			open_get_filename(filename),
			streaming = data.get('stream', False)
		)
	return audio_cache[name]


def unload():
	warnings.warn('resource.unload is experemental', FutureWarning)
	cache = {}
