Tutorial
========

This tutorial will walk you through creating your first game with Fireform.

If you haven't done so already, you should :doc:`install Fireform <install>`.

Creating The World
------------------

Starting a Fireform game requires some boilerplate code, so open up a new python file and I'll walk you through it.

The first thing that we need to do is import fireform.

.. code-block:: python

	import fireform

For the sake of completeness, all things in the library will be referenced their full name.

Immediately after importing the library, we need to specify which engine we want to use.

.. code-block:: python

	fireform.engine.load('pyglet')

Pyglet is a lightweight media library for python.

.. note::

	There are currently no other engines supported, so you don't actually get a choice here. This may seem redundant, but it's a form of future-proofing.

Next, we need to create a :doc:`world`. Worlds are used to hold all the objects in the game, and give them a space in which they can interact.

.. code-block:: python

	world = fireform.world.world()

The world won't actually do anything by itself, however. Systems are used to define the rules that govern the world. Systems would be akin to the forces of gravity and electromagnetism that govern our universe.

.. code-block:: python

	world.add_system(fireform.system.motion())
	world.add_system(fireform.system.camera())
	world.add_system(fireform.system.image())
	world.add_system(fireform.system.debug())

These four 'standard' systems serve different purposes.

The *motion* system handles the movement of objects, and detects when they collide with each other.

The *camera* system allows the viewer to move around the world. Otherwise the viewpoint (camera) would be stuck in the one location the entire time.

The *image* system is responsible for rendering graphics.

The *debug* system gives us a number of tools to examine and manipulate entities when we run the game. If you decide to release a game, this would be removed.

Finally, we have to start the game. This line will block, so make sure it is at the end of your code.

.. code-block:: python

	fireform.main.run(world)

If you run the code now you won't see much. That's because there's no entities in the game.

Creating The Player
-------------------

Add the following code to the script. Make sure it comes before ``fireform.world.run``.

.. code-block:: python

	player = fireform.entity(
		fireform.data.box(x = 0, y = 0, width = 60, height = 60)
	)

	world.add_entity(player)

The ``fireform.entity`` function accepts an arbitrary number of arguments. Each argument is a single aspect of the entity. `fireform.data.box` represents the bounding box of the entity.

If you run the code now you should see a green square in the middle of the window. This is the entity we have just created. If you hover your mouse over it you should get a description of the entity on the left hand side of the screen.

Now lets add some motion to the object. We can add a velocity component to make the entity move, and we can add an acceleration component in order to make it accelerate in a particular direction.

.. code-block:: python

	player = fireform.entity(
		fireform.data.box(x = 0, y = 0, width = 60, height = 60),
		fireform.data.velocity(7, 4),
		fireform.data.acceleration(-0.2, -0.05)
	)

If you run the game now, you should see the box move upwards and to the right, then turn around and exit on the right hand side of the screen.

.. code-block:: python

	player = fireform.entity(
		fireform.data.box(x = 0, y = 0, width = 60, height = 60),
		fireform.data.velocity(),
		fireform.data.acceleration(),
		fireform.data.friction(0.9, 0.9),
		fireform.util.behaviour_eight_direction_movement(speed = 3)
	)

.. code-block:: python

	# Load the resources. See resources.json for more details.
	fireform.resource.load('./resources/')
