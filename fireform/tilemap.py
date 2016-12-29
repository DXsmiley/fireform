import fireform.data
import fireform.entity
import fireform.engine
import fireform.resource

cache = {}

def grab_piece(image_name, image, x, y, w, h):
	t = (image_name, x, y, w, h)
	if t not in cache:
		cache[t] = image.get_region(x, y, w, h)
	return cache[t]

def create(arrays, tile_dim, image_names, ordering = 0):
	"""Creates an entity which contains all the information to display a tile map.

	arrays should be a grid specifying the tile at each location.
	tile_dim is the size of each tile (which must be square)
	image_name is the name of the texture to use to display the map
	"""
	batch = fireform.engine.current.batch()
	sprites = []
	images = []
	for i in image_names:
		width, height = fireform.resource.image_size(i)
		images.append({
			'name': i,
			'count': width // tile_dim * height // tile_dim
		})
	for x, col in enumerate(arrays):
		for y, ti in enumerate(col):
			if ti != 0:
				ti -= 1
				for k in images:
					if ti >= k['count']:
						ti -= k['count']
					else:
						image = fireform.resource.image(k['name'])
						it_width = image.width // tile_dim
						tx = (ti % it_width) * tile_dim
						ty = image.height - (((ti // it_width) + 1) * tile_dim)
						piece = grab_piece(k['name'], image, tx, ty, tile_dim, tile_dim)
						sprite = fireform.engine.current.sprite(img = piece, x = x * tile_dim, y = y * tile_dim, batch = batch)
						sprites.append(sprite)
						break;
	return fireform.entity.entity(fireform.data.image_batch(batch, sprites), ordering = ordering)
