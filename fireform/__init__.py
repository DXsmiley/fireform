"""@package fireform
Fireform is a entity-component based 2D game framework for Python.

"""

VERSION = '0.0.1'
VERSION_INTS = tuple(map(int, VERSION.split('.')))

import fireform.main
import fireform.world
import fireform.entity
import fireform.data
import fireform.system
import fireform.input
import fireform.tilemap
import fireform.resource
import fireform.util
import fireform.audio
import fireform.efilter
import fireform.geom
import fireform.engine

from fireform.entity import entity
