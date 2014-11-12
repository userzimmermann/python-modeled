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

"""modeled.range

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['range']

from operator import lt, le

from moretools import cached

from modeled import mtuple
from . import typed


class Type(typed.base.type):
    INC_FUNCTIONS = {
      str: lambda value, step: chr(ord(value) + step),
      }

    @cached
    def __getitem__(cls, mtype):
        class typedcls(cls):
            pass

        if type(mtype) is tuple:
            mtype = mtuple[mtype]
            incfuncs = tuple(
                cls.INC_FUNCTIONS.get(mt, mt.__add__)
                for mt in mtype.mtypes)
            typedcls.inc = staticmethod(lambda value, step: tuple(
              f(v, s) for f, v, s in zip(incfuncs, value, step)))
        else:
            typedcls.inc = staticmethod(
                cls.INC_FUNCTIONS.get(mtype, mtype.__add__))
        return typed.base.type.__getitem__(cls, mtype, typedcls=typedcls)

    def inclusive(cls, start, stop, step=1):
        return cls(start, stop, step, inclusive=True)

    inc = inclusive


class range(with_metaclass(Type, typed.base)):
    __module__ = 'modeled'

    def __init__(self, start, stop, step=1, inclusive=False):
        try:
            mtype = self.mtype
        except AttributeError:
            if type(start) is tuple:
                self.__class__ = type(self)[tuple(map(type, start))]
            else:
                self.__class__ = type(self)[type(start)]
        else:
            if not isinstance(start, mtype):
                start = mtype(start)
        self.start = start
        self.stop = stop
        self.step = step
        self.inclusive = inclusive

    def __iter__(self):
        mtype = self.mtype
        value, stop, step = self.start, self.stop, self.step
        check = self.inclusive and le or lt
        while check(value, stop):
            if not isinstance(value, mtype):
                value = mtype(value)
            yield value
            value = self.inc(value, step)

    def __len__(self):
        # extra iter() because list() tries .__len__() ==> endless recursion
        return len(list(iter(self)))

    def __contains__(self, value):
        return value in iter(self)

    def __array__(self, dtype=None):
        import numpy
        # extra iter() because list() tries .__len__(),
        #  which also creates list
        return numpy.array(list(iter(self)), dtype=dtype)

    def __repr__(self):
        cls = type(self)
        text = '%s.%s' % (cls.__module__, cls.__name__)
        if self.inclusive:
            text += '.inclusive'
        return text + '(%s, %s, %s)' % (
          repr(self.start), repr(self.stop), repr(self.step))
