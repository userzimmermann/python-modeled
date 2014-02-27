try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


VERSION = open('VERSION').read().strip()

REQUIRES = open('requirements.txt').read()


setup(
  name='modeled',
  version=VERSION,
  description="Universal data modeling.",

  author='Stefan Zimmermann',
  author_email='zimmermann.code@gmail.com',
  url='http://bitbucket.org/userzimmermann/python-modeled',

  license='LGPLv3',

  install_requires=REQUIRES,

  packages=[
    'modeled',
    'modeled.cfunc',
    ],

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
