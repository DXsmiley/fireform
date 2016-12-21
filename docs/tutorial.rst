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

.. code-block:: python

	# Load the resources. See resources.json for more details.
	fireform.resource.load('./resources/')
