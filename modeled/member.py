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

"""modeled.member

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = [
  'MembersDict', 'MemberError', 'member',
  'ismodeledmember', 'getmodeledmembers']

import re
from collections import OrderedDict
from inspect import isclass

from moretools import simpledict, SimpleDictStructType

import modeled
from .options import Options


class MembersDictStructType(SimpleDictStructType):
    """`basestructtype` for `simpledict()` to create MembersDict.struct class.
    """
    def __init__(self, model, members):
        def bases():
            for cls in model.__bases__:
                if cls is not object:
                    yield cls.members
        # Delegates members to SimpleDictType.__init__()
        SimpleDictStructType.__init__( # First arg is struct __name__
          self, '%s.members' % repr(model), bases(), members)


MembersDict = simpledict(
  'MembersDict', basestructtype=MembersDictStructType,
  dicttype=OrderedDict)


class MemberError(AttributeError):
    __module__ = 'modeled'

## MemberError.__name__ = 'modeled.MemberError'


# To assign a unique id the every new member instance,
# to make them orderable (incremented in member.__init__):
_memberid = 0


class Type(type):
    """Metaclass for :class:`member`.

    - Provides modeled.member[<dtype>] initialization syntax.
    """
    def __getitem__(cls, dtype):
        """Instantiate a modeled.member with given `dtype`.
        """
        return cls(dtype)

    @property
    def type(cls):
        """Get a :class:`modeled.member`'s metaclass with .type.
        """
        return type(cls)


class member(with_metaclass(Type, object)):
    """Typed data member of a :class:`modeled.object`.
    """
    __module__ = 'modeled'

    def __init__(self, type_or_value, **options):
        """Create a :class:`modeled.object` data member
           with an explicit value type or a default value with implicit type.
        """
        # First the unique member ordering id
        global _memberid
        self._id = _memberid
        _memberid += 1
        # Then set data type/default and options
        member.__call__(self, type_or_value, **options)

    def __call__(self, type_or_value, **options):
        """(Re)set value type/default and `options`.

        - If dtype was already set, default value will be converted.
        """
        if isclass(type_or_value):
            self.dtype = type_or_value
        elif self.dtype:
            self.default = self.dtype(type_or_value)
        else:
            self.dtype = type(type_or_value)
            self.default = type_or_value
        # If no explicit name is given, the associated class attribute name
        # will be used and assigned in modeled.object.type.__init__:
        self.name = options.pop('name', None)
        self.options = Options.frozen(options)
        return self

    def __get__(self, obj, owner=None):
        """Get the current member value stored in `obj.__dict__`.
        """
        if not obj: # ==> Accessed from modeled.object class level
            return self
        try:
            return obj.__dict__[self.name]
        except KeyError:
            try:
                return self.default
            except AttributeError:
                raise MemberError("'%s' has no default value." % self.name)

    def __set__(self, obj, value):
        """Store a new member `value` in `obj.__dict__`.

        - Converts value to member data type (instantiates type with value)
        """
        if type(value) is not self.dtype:
            value = self.dtype(value)
        obj.__dict__[self.name] = value

    def __repr__(self):
        repr_ = 'modeled.member[%s]' % self.dtype.__name__
        try:
            default = self.default
        except AttributeError:
            return repr_
        return repr_ + '(%s)' % repr(self.default)


def ismodeledmember(obj):
    """Checks if `obj` is an instance of :class:`modeled.member`.
    """
    return isinstance(obj, member)


def getmodeledmembers(obj, properties=True):
    """Get a list of all :class:`modeled.member` (name, instance) pairs
       of a :class:`modeleled.object` subclass
       or (name, value) pairs of a :class:`modeled.object` instance
       in member creation and inheritance order.

    :param properties: Include :class:`modeled.property` instances?
    """
    if modeled.ismodeledclass(obj):
        if properties:
            return list(obj.model.members)
        return list((name, member) for name, member in obj.model.members
                    if not modeled.ismodeledproperty(member))
    if modeled.ismodeledobject(obj):
        if properties:
            return [(name, getattr(obj, name))
                    for (name, _) in obj.model.members]
        return [(name, getattr(obj, name))
                for (name, member) in obj.model.members
                if not modeled.ismodeledproperty(member)]
    raise TypeError(
      "getmodeledmembers() arg must be a subclass or instance"
      " of modeled.object")
