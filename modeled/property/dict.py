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

"""modeled.property.dict

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

from six.moves import builtins
from itertools import chain

from moretools import istuple, isdict, cached

from modeled import mtuple
from modeled.member import member
from . import property


class Type(property.type):
    @cached
    def __getitem__(cls, mtypes):
        mkeytype, mvaluetype = mtypes
        if istuple(mkeytype):
            mkeytype = mtuple[mkeytype]
        return property.type.__getitem__(cls, mtuple[mkeytype, mvaluetype])


class DictProxy(object):
    def __init__(self, p, minstance):
        self.p = p
        self.minstance = minstance

    def __getitem__(self, key):
        """Get the current dict property key value
           via defined getter function.
        """
        if not isinstance(key, self.p.mkeytype):
            key = self.p.mkeytype(key)
        if key not in self.keys():
            raise KeyError(key)
        if not self.p.fget:
            raise type(self.p).error("'%s' has no getter." % self.p.name)
        if not istuple(key):
            key = key,
        value = self.p.fget(self.minstance, *key)
        if not isinstance(value, self.p.mvaluetype):
            value = self.p.new(value)
        if self.p.choices and value not in self.p.choices:
            raise type(self.p).error("Not a valid choice for '%s': %s" % (
              self.p.name, repr(value)))
        return value

    def __setitem__(self, key, value):
        """Pass a new list property `value` with `index`
           to the defined setter function.

        - Converts value to property data type (instantiates type with value).
        """
        if not isinstance(key, self.p.mkeytype):
            key = self.p.mkeytype(key)
        if key not in self.keys():
            raise KeyError(key)
        if not self.p.fset:
            raise type(self.p).error("'%s' has no setter." % self.p.name)
        if not isinstance(value, self.p.mvaluetype):
            value = self.p.new(value)
        if self.p.choices and value not in self.p.choices:
            raise type(self.p).error(
              "Not a valid choice for '%s': %s" % (self.p.name, repr(value)))
        if istuple(key):
            args = key + (value,)
        else:
            args = key, value
        self.p.fset(self.minstance, *args)
        # Finally call hook functions... first own (modeled class level)...
        for func in self.p.changed:
            func(self.minstance, value)
        #... then instancemember level:
        submember = self.p[key]
        try:
            # Get the instancemember for the given object...
            im = self.minstance.__dict__[submember.name]
        except KeyError:
            pass
        else:
            for func in im.changed:
                func(value)

    def update(self, mapping=(), **items):
        if isdict(mapping):
            mapping = mapping.items()
        for key, value in chain(mapping, items.items()):
            self[key] = value

    def keys(self):
        if not self.p.fkeys:
            raise type(self.p).error(
              "'%s' has no keys getter." % self.p.name)
        for key in self.p.fkeys(self.minstance):
            if not isinstance(key, self.p.mkeytype):
                key = self.p.mkeytype(key)
            yield key

    def values(self):
        for key in self.keys():
            yield self[key]

    def items(self):
        for key in self.keys():
            yield key, self[key]

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        return iter(self.keys())


class Dict(with_metaclass(Type, property)):
    @builtins.property
    def mkeytype(self):
        return self.mtype.mtypes[0]

    @builtins.property
    def mvaluetype(self):
        return self.mtype.mtypes[1]

    def __init__(self, mkeytype=None, mvaluetype=None,
                 fget=None, fset=None, fkeys=None, keys=None,
                 **options):
        if mkeytype is None and mvaluetype is None:
            assert(self.mtype)
        else:
            self.__class__ = type(self)[mkeytype, mvaluetype]
        member.__init__(self, **options)
        self.fget = fget
        self.fset = fset
        if keys is not None:
            self.fkeys = lambda self: keys
        else:
            self.fkeys = fkeys
        if self.new is self.mtype:
            self.new = self.mvaluetype

    def keys(self, fkeys):
        """The .keys decorator function.
        """
        self.fkeys = fkeys
        return self

    def __get__(self, obj, owner=None):
        if obj is None: # ==> Accessed from modeled.object class level
            return self

        return DictProxy(self, obj)

    @cached
    def __getitem__(self, key):
        if istuple(key):
            name = '%s[%s]' % (self.name, ', '.join(map(repr, key)))
        else:
            name = '%s[%s]' % (self.name, repr(key))

        @property(self.mvaluetype, name=name)
        def item(minstance):
            return DictProxy(self, minstance)[key]

        @item.setter
        def item(minstance, value):
            DictProxy(self, minstance)[key] = value

        return item

Dict.__name__ = Dict.__qualname__ = 'property.dict'
