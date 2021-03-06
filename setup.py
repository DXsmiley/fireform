from setuptools import setup
# Consistent encoding
from codecs import open
from os import path

with open('requirements.txt') as f:
	requirements = f.read().splitlines()

LONG_DESC = """
Fireform is an entity-driven game framework.
It's currently in early alpha and has minimal documentation.
The API is subject to change without notice.
"""

setup(
	name = 'fireform',
	version = '0.0.1',
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

	install_requires = requirements,
	include_package_data = True,
	packages = [
		'fireform',
		'fireform.data',
		'fireform.engine',
		'fireform.geom',
		'fireform.system',
		'fireform.util'
	]

)
