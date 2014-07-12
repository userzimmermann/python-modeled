import sys
from subprocess import call


exec(open('__init__.py').read())

if 'sdist' in sys.argv:
    status = call('scons')
    if status:
        sys.exit(status)


setup(
  name=NAME,
  version=VERSION,
  description="Universal data modeling.",

  author='Stefan Zimmermann',
  author_email='zimmermann.code@gmail.com',
  url='http://bitbucket.org/userzimmermann/python-modeled',

  license='LGPLv3',

  install_requires=REQUIRES,

  package_dir={
    'modeled.setup': '.',
    },
  packages=[
    'modeled',
    'modeled.setup',
    'modeled.member',
    'modeled.cfunc',
    ],
  package_data={
    'modeled.setup': SETUP_DATA,
    },

  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved ::'
    ' GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
    'Topic :: Utilities',
    ],
  keywords=[
    'modeled', 'model', 'modeling', 'modelled', 'modelling',
    'serialization', 'exchange', 'mapping',
    'class', 'object', 'member', 'property', 'typed',
    'ctypes', 'cfunc', 'funcptr',
    'python3',
    ],
  )
