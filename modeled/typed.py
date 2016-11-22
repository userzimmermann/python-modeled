# python-modeled
#
# Copyright (C) 2014 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# python-modeled is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-modeled is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-modeled.  If not, see <http://www.gnu.org/licenses/>.

"""modeled.typed

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['base']

import six
from six import with_metaclass
from inspect import getargspec, isclass

from decorator import decorator
from moretools import cached, qualname

import modeled


class meta(modeled.base.meta):
    """
    Base metaclass for MODELED components with a connected data type (mtype).

    * Provides ``class[mtype]`` syntax:

    >>> class typable(base):
    ...     pass

    >>> type(typable) is meta
    True

    >>> typable[int].mtype is int
    True
    """
    __qualname__ = 'meta'  # for PY2

    @property
    @cached
    def strict(cls):
        """
        Creates a derived base class with strict data type checking,
        which means:

        * No type conversions shall be performed on data processing.
        * Unmatching data types shall immediately raise ``TypeError``.

        >>> class typable(base):
        ...     pass

        >>> typable.isstrict()
        False

        >>> issubclass(typable.strict, typable)
        True

        >>> typable.strict.isstrict()
        True

        Resulting class objects are cached:

        >>> typable.strict is typable.strict
        True
        """
        class strict(cls, modeled.strict.base):
            __module__ = cls.__module__
            __qualname__ = qualname(cls) + '.strict'

            @classmethod
            def isstrict(cls):
                """
                Overwrites basic method and just returns ``True`` to denote
                strict data type checking.
                """
                return True

        return strict

    @cached
    def __getitem__(cls, _type, typedcls=None, typedbase=None):
        """
        Derive a typed subclass from `cls` with given `mtype`.

        * Optionally takes a predefined `typedcls` from a derived
          metaclass' ``.__getitem__``.
        """
        if not isclass(_type):
            raise TypeError("MODELED data types must be classes, not: %s"
                            % repr(_type))

        if typedcls is None:
            if typedbase is None:
                typedbase = cls

            class typedcls(typedbase):
                pass

        typedcls.mtype = typedcls.type = _type
        typedcls.__module__ = cls.__module__
        typedcls.__name__ = '%s[%s]' % (cls.__name__, _type.__name__)
        typedcls.__qualname__ = '%s[%s]' % (qualname(cls), _type.__name__)
        return typedcls


class base(with_metaclass(meta, modeled.base)):
    """
    Base class for all MODELED components with a connected data type (mtype).
    """
    __qualname__ = 'base'  # for PY2

    @classmethod
    def isstrict(cls):
        """
        By default, MODELED typable classes don't do strict type checking,
        so this method just returns ``False``.

        Only the ``.strict`` variants of typable classes do so.
        They are derived via :prop:`modeled.typed.meta.strict`.
        """
        return False

    def new(self, value, func):
        value = func(value)
        if isinstance(value, self.mtype):
            return value
        raise TypeError(
          "%s.new.func() must return an instance of '%s', not '%s'"
          % (qualname(type(self)), qualname(self.mtype),
             qualname(type(value))))


def typed(func=None, argtypes=None, returntype=None):
    if func is None:
        def typed(func):
            global typed
            return typed(func, argtypes, returntype)

        return typed

    if argtypes is not None or returntype is not None:
        spec = getargspec(func)
        mtypes = {} if argtypes is None else dict(argtypes)
        mtypes['return'] = returntype
    else:
        from inspect import getfullargspec
        spec = getfullargspec(func)
        mtypes = spec.annotations

    def typed(func, *args, **kwargs):
        iargs = iter(args)
        args = []
        for name, value in zip(spec.args, iargs):
            mtype = wrapper.mtypes.get(name)
            if isclass(mtype) and not isinstance(value, mtype):
                value = mtype(value)
            args.append(value)
        result = func(*args, **kwargs)
        mtype = wrapper.mtypes.get('return')
        if isclass(mtype) and not isinstance(result, mtype):
            result = mtype(result)
        return result

    wrapper = decorator(typed, func)
    wrapper.mtypes = mtypes
    return wrapper


import modeled.strict
