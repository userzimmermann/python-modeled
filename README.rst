
python-modeled
==============

.. code:: python


    >>> import modeled
    >>> print(modeled.__version__) 
    0.1


.. code:: python


    >>> print(modeled.__description__)
    Universal data modeling for Python.



-  Create `classes <#rst-header-writing-modeled-classes>`__ with typed data
   `members <#Adding-modeled-members>`__ in pythonic style.
-  Use typed containers.
-  Map modeled classes and their instances to any kind of data storage,
   serialization, visualization or user interface by using existing
   adapters or writing custom ones.



https://bitbucket.org/userzimmermann/python-modeled

https://github.com/userzimmermann/python-modeled


0. Setup
========


**Supported Python versions**: `2.7 <http://docs.python.org/2.7>`__,
`3.3 <http://docs.python.org/3.3>`__,
`3.4 <http://docs.python.org/3.4>`__

Just install the latest
`release <https://pypi.python.org/pypi/modeled>`__ with
`pip <http://www.pip-installer.org>`__. It automatically installs all
requirements:

::

    pip install modeled


.. code:: python


    >>> modeled.__requires__
    six
    path.py>=7.0
    moretools>=0.1.5



1. Writing modeled classes
==========================


All Python classes are derived from ``object``. Modeled classes are
derived from ``modeled.object``, which has a predefined ``mobject``
shortcut:


.. code:: python


    from modeled import mobject

.. code:: python


    class MClass(mobject):
        # optional
        class model:
            name = 'NotMClass'
    
            group__option = 'value'
    
            class group:
                other_option = 'other value'

Adding modeled members
~~~~~~~~~~~~~~~~~~~~~~


Modeled members are the typed attributes of modeled objects. They are
defined as modeled class attributes and connect to class instances via
Python's descriptor mechanism. These member descriptors are instances of
the ``modeled.member`` base class, which has a predefined ``m``
shortcut. Typed member subclasses are created by passing any type (class
object) in ``[...]`` brackets to the member base class:


.. code:: python


    from modeled import mobject, m

.. code:: python


    class MClass(mobject):
        some_int = m[int]
        some_float = m[float]
        some_string = m[str]


These typed member suclasses are created only once for each given type.
Modeled member descriptors are automatically instantiated by
``modeled.object``'s metaclass. You can easily access these instances on
modeled class level:


.. code:: python


    >>> MClass.some_int
    modeled.member[int]()



.. code:: python


    >>> MClass.some_int.mtype
    int




Manually instantiate a member descriptor for defining a default value or
passing extra keyword arguments or options:


.. code:: python


    class MClass(mobject):
        some_int = m[int](4, name='not_some_int', group__option='value')


Other keyword arguments are:

-  ``new=`` Any callable object which will be called instead of member's
   data type if setting a member value which is not an instance of data
   type. Must return a data type instance.
-  ``choices=`` A sequence of allowed member values.
-  ``changed=`` A sequence of callback functions (any callable objects)
   to be triggered after setting member values. Get the modeled class
   instance as first and the value as second argument.



When providing a default value, the data type can be omitted:


.. code:: python


    >>> m(4)
    modeled.member[int](4)


