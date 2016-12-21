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
	world.add_system(fireform.system.debug(allow_edit = True))

These four 'standard' systems serve different purposes.

The *motion* system handles the movement of objects, and detects when they collide with each other.

The *camera* system allows the viewer to move around the world. Otherwise the viewpoint (camera) would be stuck in the one location the entire time.

The *image* system is responsible for rendering graphics.

The *debug* system gives us a number of tools to examine and manipulate entities when we run the game.

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

If you run the code now you should see a green square in the middle of the window. This is the entity we have just created. If you hover your mouse over it you should get a description of the entity on the left hand side of the screen. You can use the left mouse button to drag the box around the screen, and the right button to resize it.

Now lets add some motion to the object. We can add a velocity component to make the entity move, and we can add an acceleration component in order to make it accelerate in a particular direction.

.. code-block:: python

	player = fireform.entity(
		fireform.data.box(x = 0, y = 0, width = 60, height = 60),
		fireform.data.velocity(7, 4),
		fireform.data.acceleration(-0.2, -0.05)
	)

If you run the game now, you should see the box move upwards and to the right, then turn around and exit on the right hand side of the screen.

For this object to actually be the 'player', the user will have to be able to control it. Remove the arguments passed to the velocity and acceleration components so that the box is initially at rest.

From here, we can add two more components to make the box controllable.

.. code-block:: python

	player = fireform.entity(
		fireform.data.box(x = 0, y = 0, width = 60, height = 60),
		fireform.data.velocity(),
		fireform.data.acceleration(),
		fireform.data.friction(0.9, 0.9),
		fireform.util.behaviour_eight_direction_movement(speed = 3)
	)

The friction component will ensure that the player doesn't reach ridiculous speeds and spiral out of control.

Unlike the other components, ``behaviour_eight_direction_movement`` is a *behaviour*. This means that it responds to events that occur and will modify the entity. This particular behaviour listens for key press events and will set the acceleration of the entity when they happen.

If you run the game now, you should be able to move the green box around the screen using the arrow keys.

You can fiddle around with the values passed to friction and the movement behaviour in order to change how the box handles.

Adding Graphics
---------------

First, you'll need an image to add to the game. Open up your favourite image editor and draw something. The image should be 60 by 60 pixels, the same size as the player object. Save the image in the same directory as the code, and call it ``my_image.png``.

.. note::
	Currently, Fireform only supports PNG image files.

Next, you'll need to create a file to describe all your resources. Create a new text file in the same directory as the code, and call it `resources.json`. Paste the following code into it.

.. code-block:: json

	{
		"images":
		{
			"my_image":
			{
				"x_offset": "50%",
				"y_offset": "50%"
			}
		}
	}

It doesn't look like much, but it will tell Fireform to load ``my_image.png``.  The ``x_offset`` and ``y_offset`` specify the image's centre. The ``"50%"`` specifies that it should be in the middle of the image. Setting it to an actual integer will specify the offset in number of pixels from the top left.

We then need to get Fireform to read this file. To do that we put the following line of code after ``fireform.engine.load('pyglet')``.

.. code-block:: python

	fireform.resource.load('.')

The function takes any number of strings, representing the directories that Fireform should search when looking for images. The ``.`` represents the working directory (the one that the code is in).

If you had some of your resources separated into folders, you would have to mention those explicitly:

.. code-block:: python

	fireform.resource.load('.', './images', './audio')

Finally, we add the image to our player entity from earlier:

.. code-block:: python

	player = fireform.entity(
		fireform.data.box(x = 0, y = 0, width = 60, height = 60),
		fireform.data.velocity(),
		fireform.data.acceleration(),
		fireform.data.friction(0.9, 0.9),
		fireform.util.behaviour_eight_direction_movement(speed = 3),
		fireform.data.image('my_image')
	)

If you run the game now you should now see your beautifully drawn picture running around the screen.

Completed Code
--------------

code.py
^^^^^^^

.. code-block:: python

	import fireform

	fireform.engine.load('pyglet')

	fireform.resource.load('.')

	world = fireform.world.world()

	world.add_system(fireform.system.motion())
	world.add_system(fireform.system.camera())
	world.add_system(fireform.system.image())
	world.add_system(fireform.system.debug(allow_edit = True))

	player = fireform.entity(
		fireform.data.box(x = 0, y = 0, width = 60, height = 60),
		fireform.data.velocity(),
		fireform.data.acceleration(),
		fireform.data.friction(0.9, 0.9),
		fireform.util.behaviour_eight_direction_movement(speed = 3),
		fireform.data.image('my_image')
	)

	world.add_entity(player)

	fireform.main.run(world)

resources.json
^^^^^^^^^^^^^^

.. code-block:: json

	{
		"images":
		{
			"my_image":
			{
				"x_offset": "50%",
				"y_offset": "50%"
			}
		}
	}
