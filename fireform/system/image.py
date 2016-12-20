import math

from fireform.system.base import base
import sortedcontainers
import fireform.resource

class image(base):
	"""This system draws images for you."""

	def __init__(self):
		self.batches = {}
		self.batch_numbers = sortedcontainers.SortedDict()
		self.filter_main = None
		self.filter_batches = None
		self.camera_system = None

	def name(self):
		return 'fireform.system.image'

	def attach(self, world):
		self.filter_main = world.filter_root.chain('box > image')
		self.filter_batches = world.filter_root.chain('image_batch')
		self.camera_system = world.systems_by_name['fireform.system.camera']

	def get_batch(self, depth):
		if depth not in self.batches:
			self.batches[depth] = fireform.engine.current.batch()
		return self.batches[depth]

	def center_image(self, image):
		image.anchor_x = image.width / 2
		image.anchor_y = image.height / 2

	def m_new_entity(self, world, message):
		if message.entity['image']:
			ordering = message.entity.ordering
			self.batch_numbers[ordering] = self.batch_numbers.get(ordering, 0) + 1

	def m_dead_entity(self, world, message):
		img = message.entity['image']
		if img and img.sprite_object:
			ordering = message.entity.ordering
			self.batch_numbers[ordering] -= 1
			if self.batch_numbers[ordering] == 0:
				del self.batch_numbers[ordering]
			img.sprite_object.opacity = 0
			img.sprite_object.flush()
			img.sprite_object.delete()
			img.sprite_object = None

	def m_draw(self, world, message):
		self.update_sprites()
		num_batches = self.sort_and_draw()
		world.post_message(fireform.message.update_tracked_value('image_batches', num_batches))

	def update_sprites(self):
		bounds = self.camera_system.boundary()
		# print('ff.system.image.m_draw')
		for i in self.filter_main:
			e_img = i[fireform.data.image]
			e_pos = i[fireform.data.box].position
			scale = fireform.geom.vectorify(e_img.scale)
			if fireform.geom.box_overlap(bounds, i.box):
				image_name = e_img.image
				if image_name != None:
					# Create the sprite object
					if e_img.sprite_object == None:
						i_obj = fireform.resource.image(image_name, int(e_img.frame))
						e_img.sprite_object = fireform.engine.current.sprite(
							img = i_obj,
							batch = self.get_batch(i.ordering),
							blend = e_img.blend
						)
						e_img.image_last = e_img.image
					# Change the sprite's image
					if e_img.image != e_img.image_last or int(e_img.frame) != e_img.frame_last:
						i_obj = fireform.resource.image(image_name, int(e_img.frame))
						e_img.sprite_object.image = i_obj
						e_img.image_last = e_img.image
					sprite = e_img.sprite_object
					if sprite:
						if e_img.scissor:
							r = e_img.scissor.box.rectangle
							m = i[fireform.data.box].rectangle
							# print(r)
							e_img.sprite_object.crop_box = (
								math.floor(max(r.left, m.left)),
								math.floor(max(r.bottom, m.bottom)),
								math.ceil(min(r.right, m.right)),
								math.ceil(min(r.top, m.top))
							)
						else:
							e_img.sprite_object.crop_box = None
						sprite.x = int(e_pos.x)
						sprite.y = int(e_pos.y)
						sprite.rotation = e_img.rotation
						sprite.scale = e_img.scale
						sprite.visible = True
						sprite.opacity = int(e_img.alpha)
						# This is an implementation detail that is required to prevent
						# pyglet doing an unholy number of extra calculations
						sprite.flush()
			else:
				if e_img.sprite_object != None:
					if e_img.sprite_object.visible:
						e_img.sprite_object.visible = False
						e_img.sprite_object.flush()
			e_img.frame_last = int(e_img.frame)
			e_img.frame += e_img.frame_speed

	def sort_and_draw(self):
		tasks = []
		self.task_setup(tasks)
		# The actual drawing of things is quite slow.
		# I might have to find a way to speed these things up somehow...
		for o, b in tasks:
			b.draw()
		return len(tasks)

	# Despite the fact that this feels really bad, it's actually pretty fast
	# since the total number of layers that I have is minimal.
	def task_setup(self, tasks):
		for batch_entity in self.filter_batches:
			tasks.append((batch_entity.ordering, batch_entity['image_batch'].batch))
			# batch_entity['image_batch'].batch.draw()
		for ordering in self.batch_numbers:
			if ordering in self.batches:
				tasks.append((ordering, self.batches[ordering]))
		tasks.sort(key = lambda x: x[0])
