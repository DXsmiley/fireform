"""

	This module loads levels made with the `tiled editor <http://www.mapeditor.org/>`_.

	The maps *must* be saved in JSON format. The standard TMX formt will not work.

"""

import fireform.tilemap
import fireform.resource
import json
import warnings
import types

class _nothing:
	pass

nothing = _nothing

def load(world, filename, loader_rules = {}, extra_data = {}, debug = False, callback = lambda w, d: None):
	""" Load a map from a file.

		:Parameters:
			`world` : :class:`fireform.world.world`
				The world to load all the entities into.
			`filename` : str
				The name of the file to load from. This does not include the extension.
				Fireform will search for the file as it would any other resource.
			`loader_rules` : dictionary of functions
				Each key should be the name of a layer. Each function should take in a single object,
				representing the information about an object in tiled. The functions should either return
				an entity, or produce an iterable of entities. The function may also return ``None``.
				Any entities produced will be added to the world.
			`extra_data` : dict
				All callback functions will be passed this as part of the data package.
			`debug` : bool
				If ``True``, debug information will be ``print``\ ed. Defaults to ``False``.

	"""
	with fireform.resource.open_data(filename + '.json') as f:
		j_data = json.loads(f.read())
		json_parse(world, j_data, loader_rules, extra_data, debug, callback)


def json_load(*args, **kwargs):
	load(*args, **kwargs)


def json_parse(world, data, loader_rules = {}, extra_data = {}, debug = False, callback = lambda w, d: None):
	data['properties'] = data.get('properties', {})
	world.width = data['width'] * data['tilewidth']
	world.height = data['height'] * data['tileheight']
	for layer in data['layers']:
		if layer.get('visible', True):
			layer_name = layer['name']
			if layer['type'] == 'objectgroup':
				if layer_name in loader_rules:
					# I'm not sure if this even does anything...
					if 'polyline' in layer:
						print('polyline!')
						for point in layer['polyline']:
							point['y'] = world.height - point['y']
					for obj in layer['objects']:
						obj['y'] = world.height - obj['y'] - obj['height']
						obj['box'] = {
							'x': obj['x'],
							'y': obj['y'],
							'width': obj['width'],
							'height': obj['height'],
							'anchor_x': 0,
							'anchor_y': 0
						}
						obj['extra'] = extra_data
						obj['everything'] = data
						obj['properties'] = obj.get('properties', {})
						# loader_rules[layer_name](world, obj)
						rule = loader_rules[layer_name]
						if isinstance(rule, str):
							# If it's a string, the object is simply a box with some tags on it
							world.add_entity(fireform.entity.entity(
								fireform.data.box(**obj['box']),
								tags = rule
							))
						else:
							result = rule(obj)
							if result is nothing:
								pass
							elif isinstance(result, list):
								for i in result:
									world.add_entity(i)
							elif isinstance(result, fireform.entity.entity):
								world.add_entity(result)
							elif isinstance(result, types.GeneratorType):
								for i in result:
									world.add_entity(i)
							else:
								warnings.warn('Cannot add {} of type {} to world (from rule: \'{}\')'.format(result, type(result), layer_name))
				else:
					warnings.warn('No known rules for {}'.format(layer_name))
			elif layer['type'] == 'tilelayer':
				# warnings.warn('Tile layers are not fully implemented.')
				height = layer['height']
				width = layer['width']
				tile_dim = data['tilewidth'] # Only supports square tiles at the moment.
				if (data['tilewidth'] != data['tileheight']):
					warnings.warn('Rectangular tiles could not be handled. Assumed they were square.')
				tdata = layer['data']
				tile_arrays = [[tdata[x + (height - y - 1) * width] for y in range(height)] for x in range(width)]
				image_name = data['tilesets'][0]['name']
				ordering = layer.get('properties', {}).get('ordering', 0)
				world.add_entity(fireform.tilemap.create(tile_arrays, tile_dim, image_name, ordering))
			elif layer['type'] == 'imagelayer':
				warnings.warn('Image layers are not fully implemented.')
				# print(json.dumps(layer, indent = 4))
				x = layer.get('offsetx', 0)
				y = world.height - layer.get('offsety', 0)
				# image = layer['image'].replace('.png', '')
				image = layer['name']
				image_object = fireform.resource.image(image)
				box = fireform.data.box(width = image_object.width, height = image_object.height)
				box.left = x
				box.top = y
				world.add_entity(fireform.entity.entity(
					box,
					fireform.data.image(image),
					ordering = layer.get('properties', {}).get('ordering', 0),
					tags = 'no-collision no-debug'
				))
			else:
				print('Cannot handle layer type', layer['type'])
		else:
			warnings.warn('Invisible layers not loaded')
	callback(world, data)

def unravel_polyline(polyline):
	""" Unravel a polyline, producing a number of intervals.

		Generates tuples, each containing two co-ordinate pairs.

		.. code:: python

			# Example usage as a loader rule
			def make_slope(obj):
				for (x1, y1), (x2, y2) in tiled.unravel_polyline(obj):
					yield fireform.entity(...)


	"""
	x = polyline['x']
	y = polyline['y']
	polyline = polyline['polyline']
	for i, j in zip(polyline[:-1], polyline[1:]):
		yield (
			(x + i['x'], y - i['y']),
			(x + j['x'], y - j['y'])
		)
