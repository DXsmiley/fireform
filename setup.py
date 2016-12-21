from setuptools import setup, find_packages
# Consistent encoding
from codecs import open
from os import path

import fireform

LONG_DESC = """
Fireform is an entity-driven game framework.
It's currently in early alpha and has minimal documentation.
The API is subject to change without notice.
"""

setup(
	name = 'fireform',
	version = fireform.VERSION,
	# url = 'https://github.com/DXsmiley/edgy-json',
	author = 'DXsmiley',
	author_email = 'dxsmiley@hotmail.com',
	# license = 'MIT',

	description = 'An entity-driven game framework.',
	long_description = LONG_DESC,

	classifiers = [
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		# 'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
	],

	keywords = 'game',

	include_package_data = True,

	packages = find_packages()

	# py_modules = [
	# 	'ff_animation_view'
	# ]
)
