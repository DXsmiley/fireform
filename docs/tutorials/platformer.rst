Platformer
==========

This tutorial will walk you through making a simple platformer game. It is assumed that you've followed the :doc:`previous tutorial <first_project>`

.. warning::

	This tutorial is incomplete.

Boilerplate
-----------

Here's the framework you'll need to get started. It should be somewhat familiar to you. The key difference is that the ``motion`` system has an additional parameter passed to it, ``collision_mode = 'split'``. This seperates the collision detection step into two phases and helps us to determine what direction an object is moving when it collides with another.

.. code-block:: python

	import fireform

	fireform.engine.load('pyglet')

	fireform.resource.load('.')

	world = fireform.world.world()

	world.add_system(fireform.system.motion(collision_mode = 'split'))
	world.add_system(fireform.system.camera())
	world.add_system(fireform.system.image())
	world.add_system(fireform.system.debug(allow_edit = True))

	# We'll put the cool stuff here.

	fireform.main.run(world)

Creating the Platforms
----------------------

The player is going to need something to jump around on, so we'll create the platforms first.

We'll make a function to create them.

.. code-block:: python

	def make_platform(x, y, width, height):
		return fireform.entity(
			fireform.data.box(x = x, y = y, width = width, height = height),
			fireform.data.collision_bucket(extrovert = True),
			tags = 'solid'
		)

Note that the x and y values specify the centre of the object.

The ``collision_bucket`` component is used to specify some rules regarding what the object can and cannot collide with. We don't actually specify a bucket here so it will use the default one. We *do* however, specify that the entity is extroverted. Extroverted entities cannot collide with other extroverted entities.

.. note::

	You don't need to specify a collision bucket for every entity. Entities without a ``collision_bucket`` component will be placed in the default bucket, and are considered to not be extroverted.

The last line tags the entity as ``'solid'`` so that we can identify what it is once the player collides with it.

We can then create platforms and add them to the world.

.. code-block:: python

	world.add_entity(make_platform(0, 0, 400, 30))
	world.add_entity(make_platform(200, 100, 180, 10))
	world.add_entity(make_platform(-200, 150, 180, 10))

If you run the game now you should see three green rectangles representing the platforms. Note that the green border is being produced by the debugging features.

.. note::

	You can press ``tab`` while running the game to toggle the debug overlay.

A falling box
-------------

Here's the hard part. We need to define what the player should do when it runs into a wall, from any direction.

The following block of code is what is known as a *behaviour*. Behaviours in fireform need to inherit from the specified base class.

The functions that start with ``m_`` are called when certain messages are send to the entity. Excluding the ``self`` argument, they all take three arguments:

- ``world`` : The world that transmitted the message.
- ``entity`` : The entity the behaviour is attached to.
- ``message`` : The message itself.

.. code-block:: python

	class platformer(fireform.behaviour.base):

		def __init__(self):
			self.on_ground = True

		def m_tick(self, world, entity, message):
			if entity.velocity.y != 0:
				self.on_ground = False

		def m_collision(self, world, entity, message):
			other = message.other
			if 'solid' in other.tags:
				if message.direction == 'horisontal':
					if entity.velocity.x > 0: # Moving to the right
						entity.box.right = other.box.left
					if entity.velocity.x < 0: # Moving to the left
						entity.box.left = other.box.right
					entity.velocity.x = 0
				if message.direction == 'vertical':
					if entity.velocity.y > 0: # Moving upwards
						entity.box.top = other.box.bottom
					if entity.velocity.y < 0: # Moving downwards
						entity.box.bottom = other.box.top
						self.on_ground = True
					entity.velocity.y = 0

``m_tick`` is fired on each and every game step. It's ``message`` parameter doesn't actually contain any data. Here, we check if the object is moving vertically. If it is, then we know that it's not sitting on the ground.

``m_collision`` is fired during every game tick where the entity is overlaping with another. ``message.other`` is the entity that it overlaps with. ``message.direction`` is a string that can be used to figure out which the way in which the entities hit each other.

If we attach this behaviour (and a few other things) to an entity, we can see it in action.

.. code-block:: python

	world.add_entity(fireform.entity(
		fireform.data.box(x = 0, y = 100, width = 60, height = 60),
		fireform.data.velocity(),
		fireform.data.acceleration(0, -0.3),
		platformer()
	))

You should see a box accelerate downwards and come to rest on the ground.

User input
----------

Create another behaviour to handle the user input.

.. code-block:: python

	class controller(fireform.behaviour.base):

		def m_key_press(self, world, entity, message):
			if message.key == fireform.input.key.LEFT:
				entity.acceleration.x -= 2
			if message.key == fireform.input.key.RIGHT:
				entity.acceleration.x += 2
			if message.key == fireform.input.key.SPACE:
				if entity[platformer].on_ground:
					entity[platformer].on_ground = False
					entity.velocity.y = 15

		def m_key_release(self, world, entity, message):
			if message.key == fireform.input.key.LEFT:
				entity.acceleration.x += 2
			if message.key == fireform.input.key.RIGHT:
				entity.acceleration.x -= 2

Change player entity:

.. code-block:: python

	world.add_entity(fireform.entity(
		fireform.data.box(x = 0, y = 300, width = 60, height = 60),
		fireform.data.velocity(),
		fireform.data.acceleration(0, -0.7),
		fireform.data.friction(0.8, 1),
		platformer(),
		controller()
	))

If you run the game you should be able to move using the arrow keys and the space bar.
