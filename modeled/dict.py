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

from modeled import mtuple
from . import typed


class Type(typed.base.type):
    __module__ = 'modeled'

    @cached
    def __getitem__(cls, mtypes):
        return typed.base.type.__getitem__(cls, mtuple[mtypes])

Type.__name__ = 'dict.type'


class dict(with_metaclass(Type, typed.base, builtins.dict)):
    __module__ = 'modeled'

    @property
    def mkeytype(self):
        return self.mtype.mtypes[0]

    @property
    def mvaluetype(self):
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
        if not isinstance(key, self.mkeytype):
            key = self.mkeytype(key)
        if not isinstance(value, self.mvaluetype):
            value = self.mvaluetype(value)
        builtins.dict.__setitem__(self, key, value)

    def update(self, iterable):
        def items():
            for key, value in iterable:
                if isinstance(key, self.mkeytype):
                    key = self.mkeytype(key)
                if isinstance(value, self.mvaluetype):
                    value = self.mvaluetype(value)
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
