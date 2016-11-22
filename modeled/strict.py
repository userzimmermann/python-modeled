# MODELED | Universal data modeling for Python
#
# Copyright (C) 2014-2016 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# MODELED is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MODELED is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with MODELED.  If not, see <http://www.gnu.org/licenses/>.

"""modeled.strict

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
import builtins
from inspect import isclass

import modeled

from . import typed


class StrictTypeError(TypeError):
    """
    Argument is not an instance of a MODELED strict data type.
    """


class meta(typed.meta):
    """
    Metaclass for :class:`modeled.strict`:

    * Provides ``strict[...]`` syntax for wrapping other classes.
    * Defines :class:`modeled.strict.base`.
    * Defines :meth:`.__subclasscheck__` for making classes derived from
      ``strict.base`` appear as subclasses of ``strict``.

    See :class:`modeled.strict` for more information and examples.
    """
    __qualname__ = 'strict.meta'

    TypeError = StrictTypeError

    class base(modeled.base):
        """
        Base class for :class:`modeled.strict` and classes created by
        :prop:`modeled.typed.meta.strict`.
        """
        __qualname__ = 'strict.base'

    def __subclasscheck__(cls, subcls):
        """
        Makes all classes derived from :class:`modeled.strict.base` appear
        as subclasses of :class:`modeled.strict`, so that ``strict[...]``
        wrapper classes don't need to be derived from ``strict``, which could
        cause conflicts with the wrapped classes, and which would keep the
        meta :meth:`.__getitem__`, which is not appropriate after wrapping.
        """
        return issubclass(subcls, cls.base)

    def __getitem__(cls, _type):

        if not isclass(_type):
            raise TypeError("MODELED data types must be classes, not: %s"
                            % repr(_type))

        metabases = type(cls.base),
        # check if we need to explicitly derive from wrapped type's metaclass
        if not issubclass(type(cls.base), type(_type)):
            metabases += type(_type),

        class typedmeta(*metabases):
            pass

        Error = cls.TypeError

        class typedcls(_type, cls.base, metaclass=typedmeta):
            """
            MODELED strict wrapper for %s, allowing instantiation only
            with instances of %s, useful for data type validation.
            """
            def __new__(cls, value):
                if not isinstance(value, _type):
                    raise Error("%s is not an instance of %s"
                                % (repr(value), repr(_type)))
                return _type.__new__(cls, value)

        typedcls.__doc__ %= repr(_type), repr(_type)
        typedcls.__name__ = '%s[%s]' % (cls.__name__, _type.__name__)
        typedcls.__qualname__ = '%s[%s]' % (cls.__qualname__, _type.__name__)
        typedmeta.__name__ = typedcls.__name__ + '.meta'
        typedmeta.__qualname__ = typedcls.__qualname__ + '.meta'
        return super(meta, cls).__getitem__(_type, typedcls=typedcls)


class strict(typed.base, meta.base, metaclass=meta):
    """
    Wraps other classes to allow instantiation only with values that are
    already instances of the wrapped class:

    >>> modeled.strict[str](3)
    Traceback (most recent call last):
      ...
    modeled.strict.StrictTypeError: ...

    ``strict[...]`` classes directly inherit from their wrapped class:

    >>> issubclass(modeled.strict[str], str)
    True

    >>> instance = modeled.strict[str]("MODELED")
    >>> isinstance(instance, str)
    True
    >>> instance.lower()
    'modeled'

    ``strict[...]`` classes don't inherit from ``strict`` but appear as
    subclasses for convenience:

    >>> modeled.strict in modeled.strict[int].mro()
    False
    >>> issubclass(modeled.strict[int], modeled.strict)
    True

    Also classes with custom metaclasses can be wrapped:

    >>> class Meta(type):
    ...     pass

    >>> class Class(metaclass=Meta):
    ...     pass

    >>> modeled.strict[Class]
    <class 'modeled.strict.strict[Class]'>
    """
