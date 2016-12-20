import fireform.behaviour
import fireform.entity

class timer(fireform.behaviour.base):

	def __init__(self, generator):
		self.generator = generator
		self.delay = 0
		self.complete = False
		self.update()

	def m_tick(self, world, entity, message):
		if self.complete:
			if entity.alive:
				entity.kill()
		else:
			self.update()

	def update(self):
		try:
			self.delay -= 1
			while self.delay <= 0:
				self.delay = next(self.generator)
				if not isinstance(self.delay, int):
					m = 'Expected int from generator function {}, got {} instead.'.format(self.generator, self.delay)
					raise TypeError(m)
				# assert(isinstance(self.delay, int))
		except StopIteration:
			self.complete = True


def create(generator):
	return fireform.entity.entity(timer(generator), tags = 'timer')


def create_slim(generator):
	t = timer(generator)
	return None if t.complete else fireform.entity.entity(t, tags = 'timer')
