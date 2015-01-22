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
  'InstanceMembersDict', 'instancemember',
  'ismodeledmemberclass', 'ismodeledmember',
  'ismodeledinstancemember',
  'getmodeledmembers']

from six.moves import builtins
from inspect import isclass
from collections import OrderedDict

from moretools import cached, simpledict

import modeled
from modeled.options import Options
from modeled.model import modelbase
from modeled import typed

from .handlers import Handlers
from .context import context


class MembersDictStructBase(simpledict.structbase):
    """`basestructtype` for `simpledict()` to create MembersDict.struct class.
    """
    def __init__(self, model, members):
        def bases():
            for cls in model.__bases__:
                if cls is not modelbase:
                    yield cls.members
        # Delegates members to SimpleDictType.__init__()
        simpledict.structbase.__init__( # First arg is struct __name__
          self, '%s.members' % repr(model), bases(), members)

    def __call__(self, properties=True):
        if properties:
            return iter(self)

        def members():
            for name, member in self:
                if not modeled.ismodeledproperty(member):
                    yield name, member

        return members()


MembersDict = simpledict(
  'MembersDict', structbase=MembersDictStructBase, dicttype=OrderedDict)


class MemberError(AttributeError):
    __module__ = 'modeled'

## MemberError.__name__ = 'modeled.MemberError'


# To assign a unique id the every new member instance,
# to make them orderable (incremented in member.__init__):
_memberid = 0


class Type(typed.base.type):
    """Metaclass for :class:`member`.

    - Provides modeled.member[<mtype>], ...[<choices>] (==> implicit mtype)
      and ...[<mtype>][<choices>] syntax.
    - Stores member (sub)class specific exception class.
    """
    __module__ = 'modeled'

    # To make the member exception class overridable in derived member types:
    error = MemberError

    def __getitem__(cls, mtype_or_choices, typedcls=None, choicecls=None):
        """Dynamically create a derived typed member class
           and optionally a further derived class with member value choices.

        - Member value type can be implicitly determined from choices.
        - Override __getitem__ methods in derived classes
          can optionally provide a precreated `typedcls` or `choicecls`.
        """
        if type(mtype_or_choices) is builtins.tuple:
            choices = mtype_or_choices
            try: # Is member cls already typed?
                cls.mtype
            except AttributeError:
                mtype = type(choices[0])
                cls = typed.base.type.__getitem__(cls, mtype, typedcls)

            if not choicecls:
                class choicecls(cls):
                    pass

            choicecls.choices = choices = builtins.list(choices)
            choicecls.__module__ = cls.__module__
            choicecls.__name__ = '%s%s' % (cls.__name__, choices)
            return choicecls

        mtype = mtype_or_choices
        return typed.base.type.__getitem__(cls, mtype, typedcls)

Type.__name__ = 'member.type'


class member(with_metaclass(Type, typed.base)):
    """Base class for typed data members of a :class:`modeled.object`.
    """
    __module__ = 'modeled'

    def __init__(self, *default, **options):
        """Create a typed :class:`modeled.object` data member
           with an optional `default` value with implicit type.
        """
        # First the unique member ordering id
        global _memberid
        self._id = _memberid
        _memberid += 1
        try:
            self.strict
        except AttributeError:
            self.strict = bool(options.pop('strict', False))
        # Then set data type/default and options
        try:
            mtype = self.mtype
        except AttributeError:
            assert(len(default) == 1)
            default = self.default = default[0]
            self.__class__ = type(self)[type(default)]
        else:
            if default:
                self.default = mtype(*default)
        try:
            options = options['options']
        except KeyError:
            pass
        try:
            newfunc = options.pop('new')
        except KeyError:
            self.new = self.mtype
        else:
            new = self.new
            self.new = lambda value, func=newfunc: new(value, func)
            self.new.func = newfunc
        try:
            changed = options.pop('changed')
        except KeyError:
            self.changed = Handlers()
        else:
            self.changed = Handlers(changed)
        # If no explicit name is given, the associated class attribute name
        # will be used and assigned in modeled.object.type.__init__:
        self.name = options.pop('name', None)
        self.title = options.pop('title', None)
        self.format = options.pop('format', None)
        try: # Were choices already defined on class level?
            self.choices
        except AttributeError:
            choices = options.pop('choices', None)
            self.choices = choices and builtins.list(choices)
        self.options = Options.frozen(options)

    def __get__(self, obj, owner=None):
        """Get the current member value (stored in `obj.__dict__`).
        """
        if obj is None: # ==> Accessed from modeled.object class level
            return self
        # Get the instancemember for the given object...
        im = obj.__dict__[self.name]
        try: #... which acts as value storage:
            return im._
        except AttributeError:
            try:
                return self.default
            except AttributeError:
                raise type(self).error(
                  "'%s' has no default value." % self.name)

    def __set__(self, obj, value):
        """Store a new member `value` (in `obj.__dict__`).

        - If not strict, converts value to member data type
          (instantiates type with value).
        - Calls `changed` hook functions.
        """
        if value is not None and not isinstance(value, self.mtype):
            if self.strict:
                raise TypeError("%s got a %s value." % (
                  repr(self), type(value)))
            value = self.new(value)
        if self.choices and value not in self.choices:
            raise type(self).error(
              "Not a valid choice for '%s': %s" % (self.name, repr(value)))
        # Get the instancemember for the given object...
        im = obj.__dict__[self.name]
        im._ = value #... which also acts as value storage
        # Finally call hook functions... first own (modeled class level)...
        for func in self.changed:
            func(obj, value)
        #... then instancemember level:
        for func in im.changed:
            func(value)

    def __repr__(self):
        repr_ = 'modeled.' + type(self).__name__
        try:
            default = self.default
        except AttributeError:
            return repr_ + '()'
        return repr_ + '(%s)' % repr(default)

    def istuple(self):
        return issubclass(self.mtype, mtuple)

    def islist(self):
        return issubclass(self.mtype, mlist)

    def isdict(self):
        return issubclass(self.mtype, mdict)


class InstanceMembersDictBase(simpledict.base):
    def __call__(self, mapping=None, **membervalues):
        return context(self, mapping, **membervalues)


InstanceMembersDict = simpledict('InstanceMembersDict',
  base=InstanceMembersDictBase, dicttype=OrderedDict)


class instancemember(object):
    def __init__(self, m, minstance):
        self.m = m
        self.minstance = minstance
        self.changed = Handlers()

    @property
    def name(self):
        return self.m.name

    @property
    def title(self):
        return self.m.title

    @property
    def value(self):
        return self.m.__get__(self.minstance)

    @value.setter
    def value(self, value):
        return self.m.__set__(self.minstance, value)

    @cached
    def __getitem__(self, key):
        return type(self)(self.m[key], self.minstance)

    def __iter__(self):
        raise TypeError("modeled.instancemember is not iterable")

    def __repr__(self):
        return 'instancemember(%s)' % repr(self.m)


def ismodeledmemberclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.member`.
    """
    if not isclass(cls):
        return False
    return issubclass(cls, member)


def ismodeledmember(obj):
    """Checks if `obj` is an instance of :class:`modeled.member`.
    """
    return isinstance(obj, member)


def ismodeledinstancemember(obj):
    """Checks if `obj` is an instance of :class:`modeled.instancemember`.
    """
    return isinstance(obj, instancemember)


def getmodeledmembers(obj, properties=True):
    """Get a list of all :class:`modeled.member` (name, instance) pairs
       of a :class:`modeleled.object` subclass
       or (name, value) pairs of a :class:`modeled.object` instance
       in member creation and inheritance order.

    :param properties: Include :class:`modeled.property` instances?
    """
    if modeled.ismodeledclass(obj):
        if properties:
            return builtins.list(obj.model.members)
        return [(name, m) for name, m in obj.model.members
                if not modeled.ismodeledproperty(m)]
    if modeled.ismodeledobject(obj):
        if properties:
            return [(name, getattr(obj, name))
                    for (name, _) in obj.model.members]
        return [(name, getattr(obj, name))
                for (name, im) in obj.model.members
                if not modeled.ismodeledproperty(im.m)]
    raise TypeError(
      "getmodeledmembers() arg must be a subclass or instance"
      " of modeled.object")


from .tuple import mtuple, Tuple
member.tuple = Tuple

from .list import mlist, List
member.list = List

from .dict import mdict, Dict
member.dict = Dict
