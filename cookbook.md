# Fireform Cookbook

This file contains a lot of snippets that will be useful to get your project up and running.

## Settings up the folder

```
mkdir my_project
mkdir my_project/resources
touch my_project/__main__.py
```

## Put stuff into `__main__.py`

```python
import fireform

# Load the resources. See resources.json for more details.
fireform.resource.load('./my_project/resources/')

# Create the world
world = fireform.world.world()
world.add_system(fireform.system.motion()) # Moves things
world.add_system(fireform.system.image())  # Needed to draw images
world.add_system(fireform.system.camera()) # Needed to view the world
world.add_system(fireform.system.debug(allow_edit = True))  # Debug info

# Add objects here

def make_focus():
	return fireform.entity.entity(
		fireform.data.box(0, 0),
		fireform.data.camera()
	)

world.add_entity(make_focus())

# Run the game
fireform.main.run(world)

```

## Mapping between the mouse cursor and in-world positions

## Setting up `resources.json`



## Debugging system

In-game controls:

Left click to pick up an object, click again to drop it.

Right click to select an object to resize, right click again to stop resizing it.

Press tab to toggle the debug display.

Press enter to enter and execute python code.

## Message reference

### m_key_press

- key
- modifiers

### m_mouse_click

- x
- y
- button

## Debugging

### Show warnings

`python -W once -m my_game`

### Profile things

`python -m cProfile -s sort my_game/__main__.py > profile.txt`

#### Possible Sort Values:

| Argument | Meaning |
| --- | --- |
| `calls` | call count |
| `cumulative` | cumulative time |
| `file` | file name |
| `ncalls` | call count |
| `pcalls` | primitive call count |
| `line` | line number |
| `name` | function name |
| `nfl` | name/file/line |
| `stdname` | standard name |
| `time` | internal time |

## Filter Notation

### Datum / Behaviour

Just use the name of it.

	box

### Multiple requirements

Put them next to each other, although it's probably better to just use a chain.

	box velocity

### Chain

Use the `>` symbol.

	box > velocity

### Tags

Use the name and a `#`.

	#solid

### Invert

Preceed the rule with a `-`.

	-box -#solid
