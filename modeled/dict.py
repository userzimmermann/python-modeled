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

"""modeled.dict

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['dict', 'ismodeleddictclass', 'ismodeleddict']

from six.moves import builtins

from moretools import cached

import modeled
from . import typed


class Type(typed.base.type):
    __module__ = 'modeled'

    @cached
    def __getitem__(cls, types):
        keytype, valuetype = types
        return typed.base.type.__getitem__(
            cls, modeled.tuple[keytype, valuetype])

    @property
    def itemtype(cls):
        return cls.mtype

    @property
    def keytype(cls):
        return cls.mtype.mtypes[0]

    @property
    def valuetype(cls):
        return cls.mtype.mtypes[1]

Type.__name__ = 'dict.type'


class dict(with_metaclass(Type, typed.base, builtins.dict)):
    __module__ = 'modeled'

    @property
    def itemtype(self):
        return self.mtype

    @property
    def keytype(self):
        return self.mtype.mtypes[0]

    @property
    def valuetype(self):
        return self.mtype.mtypes[1]

    def __init__(self, iterable=()):
        items = iter(iterable)
        try:
            self.mtype
        except AttributeError:
            try:
                key, value = next(items)
            except StopIteration:
                raise TypeError
            self.__class__ = type(self)[type(key), type(value)]
            self[key] = value
        self.update(items)

    def __setitem__(self, key, value):
        if not isinstance(key, self.keytype):
            key = self.keytype(key)
        if not isinstance(value, self.valuetype):
            value = self.valuetype(value)
        builtins.dict.__setitem__(self, key, value)

    def update(self, iterable):
        def items():
            for key, value in iterable:
                if isinstance(key, self.keytype):
                    key = self.keytype(key)
                if isinstance(value, self.valuetype):
                    value = self.valuetype(value)
                yield (key, value)

        builtins.dict.update(self, items())


def ismodeleddictclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.dict`.
    """
    try:
        return issubclass(cls, dict)
    except TypeError: # No class at all
        return False


def ismodeleddict(obj):
    """Checks if `obj` is an instance
       of :class:`modeled.dict` (or a derived class).
    """
    return isinstance(obj, dict)
