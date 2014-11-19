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

"""modeled.property.list

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from moretools import cached

from modeled.member import member
from . import property


class ListProxy(object):
    def __init__(self, p, minstance):
        self.p = p
        self.minstance = minstance

    def __getitem__(self, index):
        """Get the current list property value at given `index`
           via defined getter function.
        """
        index = int(index)
        if not index < len(self):
            raise IndexError("Index out of range: %d" % index)
        if not self.p.fget:
            raise type(self.p).error("'%s' has no getter." % self.p.name)
        value = self.p.fget(self.minstance, index)
        if not isinstance(value, self.p.mtype):
            value = self.p.new(value)
        if self.p.choices and value not in self.p.choices:
            raise type(self.p).error("Not a valid choice for '%s': %s" % (
              self.p.name, repr(value)))
        return value

    def __setitem__(self, index, value):
        """Pass a new list property `value` with `index`
           to the defined setter function.

        - Converts value to property data type (instantiates type with value).
        """
        if not index < len(self):
            raise IndexError("Index out of range: %d" % index)
        if not self.p.fset:
            raise type(self.p).error("'%s' has no setter." % self.p.name)
        if not isinstance(value, self.p.mtype):
            value = self.p.new(value)
        if self.p.choices and value not in self.p.choices:
            raise type(self.p).error(
              "Not a valid choice for '%s': %s" % (self.p.name, repr(value)))
        self.p.fset(self.minstance, index, value)

    def __len__(self):
        if not self.p.flen:
            raise type(self.p).error(
              "'%s' has no len getter." % self.p.name)
        return self.p.flen(self.minstance)

    def __iter__(self):
        for index in range(len(self)):
            yield self[index]


class List(property):
    def __init__(self, mtype=None, fget=None, fset=None,
                 flen=None, len=None,
                 **options):
        if mtype is None:
            assert(self.mtype)
        else:
            self.__class__ = type(self)[mtype]
        member.__init__(self, **options)
        self.fget = fget
        self.fset = fset
        if len is not None:
            self.flen = lambda self: len
        else:
            self.flen = flen

    def len(self, flen):
        """The .len decorator function.
        """
        self.flen = flen
        return self

    def __get__(self, obj, owner=None):
        if obj is None: # ==> Accessed from modeled.object class level
            return self

        return ListProxy(self, obj)

    @cached
    def __getitem__(self, index):
        @property(self.mtype, name='%s[%i]' % (self.name, index))
        def item(minstance):
            return ListProxy(self, minstance)[index]

        @item.setter
        def item(minstance, value):
            ListProxy(self, minstance)[index] = value

        return item

List.__name__ = List.__qualname__ = 'property.list'
