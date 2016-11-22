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

"""modeled.tuple

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['tuple', 'ismodeledtupleclass', 'ismodeledtuple']

from six import with_metaclass
from six.moves import builtins

from moretools import cached

from . import typed


class meta(typed.base.meta):
    __qualname__ = 'tuple.meta'

    @cached
    def __getitem__(cls, types, typedcls=None):
        if not typedcls:
            class typedcls(cls):
                pass

        typedcls.mtypes = typedcls.types = types = builtins.tuple(types)
        typedcls.__module__ = cls.__module__
        typedcls.__name__ = '%s[%s]' % (
            cls.__name__, ', '.join(t.__name__ for t in types))
        typedcls.__qualname__ = '%s[%s]' % (
            cls.__qualname__, ', '.join(t.__name__ for t in types))
        return typedcls


class tuple(with_metaclass(meta, typed.base, builtins.tuple)):
    __module__ = 'modeled'

    def __new__(cls, iterable):
        items = builtins.tuple(iterable)
        try:
            cls.mtypes
        except AttributeError:
            cls = cls[builtins.tuple(map(type, items))]
            return builtins.tuple.__new__(cls, items)

        assert(len(cls.mtypes) == len(items))
        items = (mtype(item) for mtype, item in zip(cls.mtypes, items))
        return builtins.tuple.__new__(cls, items)


def ismodeledtupleclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.tuple`.
    """
    try:
        return issubclass(cls, tuple)
    except TypeError: # No class at all
        return False


def ismodeledtuple(obj):
    """Checks if `obj` is an instance
       of :class:`modeled.tuple` (or a derived class).
    """
    return isinstance(obj, tuple)
