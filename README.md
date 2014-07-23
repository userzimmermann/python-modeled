modeled
=======

Universal data modeling for [Python](http://python.org).


# 0. Setup
----------

Supported __Python__ versions: __2.7__, __3.3__, __3.4__

### Requirements

* [`six`](
    https://pypi.python.org/pypi/six)
* [`path.py`](
    https://pypi.python.org/pypi/path.py)
* [`moretools>=0.1a38`](
    https://pypi.python.org/pypi/moretools)

### Installation

    python setup.py install

Or with [pip](http://www.pip-installer.org):

    pip install .

Or get the latest release from [PyPI](
  https://pypi.python.org/pypi/modeled):

    pip install modeled


# 1. Writing modeled classes
----------------------------

All Python classes are derived from `object`.
Modeled classes are derived from `modeled.object`,
which has a predefined `mobject` shortcut:

    from modeled import mobject

    class MClass(mobject):
        # optional
        class model:
            name = 'NotMClass'

            group__option = 'value'

            class group:
                other_option = 'other value'
                ...
            ...
        ...

### Adding modeled members

Modeled members are the typed attributes of modeled objects.
They are defined as modeled class attributes
and connect to class instances via Python's descriptor mechanism.
These member descriptors are instances of the `modeled.member` base class,
which has a predefined `m` shortcut.
Typed member subclasses are created by passing any type (class object)
in `[...]` brackets to the member base class:

    from modeled import mobject, m

    class MClass(mobject):
        some_int = m[int]
        some_float = m[float]
        some_string = m[str]
        some_custom = m[<user-defined class>]
        ...

These typed member suclasses are created only once for each given type.
Modeled member descriptors are automatically instantiated
by `modeled.object`'s metaclass.
You can easily access these instances on modeled class level:

    >>> MClass.some_int
    modeled.member[int]()

Manually instantiate a member descriptor for defining a default value,
or passing extra keyword arguments or options:

    class MClass(mobject):
        some_int = m[int](4, name='not_some_int', ..., group__option='value')

When providing a default value, the data type can be omitted:

    >>> m(4)
    modeled.member[int](4)

Other keyword arguments are:

* `new`:
  Any callable object which will be called instead of member's data type
  if setting a member value which is not an instance of data type.
  Must return a data type instance.
* `choices`:
  A sequence of allowed member values.
* `changed`:
  A sequence of callback functions (any callable objects)
  to be triggered after setting member values.
  Get the modeled class instance as first and the value as second argument.