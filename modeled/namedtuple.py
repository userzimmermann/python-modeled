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

"""modeled.namedtuple

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['namedtuple']

import sys
import collections

from moretools import cached

from modeled import mtuple
from . import typed


class Type(mtuple.type):
    __module__ = 'modeled'

    @cached
    def __getitem__(cls, mtypes, typedcls=None):
        mtypes = tuple(mtypes)
        assert(len(mtypes) == len(cls._fields))
        return mtuple.type.__getitem__(cls, mtypes, typedcls)


def namedtuple(typename, names):
    basetuple = collections.namedtuple(typename, names)

    class namedtuple(with_metaclass(Type, typed.base, basetuple)):
        def __new__(cls, iterable=(), **fields):
            if fields:
                items = tuple(item[1] for item in sorted(
                  fields.items(),
                  key=lambda item: cls._fields.index(item[0])))
            else:
                items = tuple(iterable)
            try:
                cls.mtypes
            except AttributeError:
                cls = cls[tuple(map(type, items))]
                return tuple.__new__(cls, items)

            assert(len(cls.mtypes) == len(items))
            items = tuple( # <-- pre-evaluate generator
              # to avoid misleading TypeError from __new__ below
              # (compalaining about missing args,
              #  although problem is mtype(item) conversion)
              mtype(item) for mtype, item in zip(cls.mtypes, items))
            return basetuple.__new__(cls, items)

    try: # Taken from collections.py:
        namedtuple.__module__ = sys._getframe(1).f_globals.get(
          '__name__', '__main__')
    except (AttributeError, ValueError):
        pass

    namedtuple.__name__ = typename
    return namedtuple
