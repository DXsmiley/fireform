Installation
============

System Requirements
-------------------

Fireform is currently being developed and tested with Python 3.5.1, but python versions 3.4 and upward should work.

Installing Fireform
-------------------

Fireform is currently in pre-alpha. Because of this, there's no PYPI entry yet.
You can install the very latest version from the git repository with the following command:

::

	pip install https://github.com/DXsmiley/fireform/archive/master.zip

Installing Engines
------------------

Fireform is designed so that it can work with a variety of backends, referred to as *engines*.

The engine handles the image loading, rendering, window creation and user input.

Currently, pyglet 1.2.4 is the only supported backend. Fireform ships with pyglet so you don't have to install it separately.
