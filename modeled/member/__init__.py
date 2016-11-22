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

from .error import MemberError
from .meta import meta
from .instancemember import instancemember
from .context import context


class MembersDictStructBase(simpledict.structbase):
    """
    ``structbase`` for ``moretools.simpledict()`` to create
    :class:`modeled.MembersDict.struct` class.
    """
    def __init__(self, model, members):
        bases = (cls.members for cls in model.__bases__
                 if cls is not modelbase)
        super(MembersDictStructBase, self).__init__(
            # first arg is .struct.__name__
            '%s.members' % repr(model), bases, members)

    def __call__(self, properties=True):
        if properties:
            return iter(self)

        return ((name, member) for name, member in self
                if not modeled.ismodeledproperty(member))


MembersDict = simpledict(
    'MembersDict', structbase=MembersDictStructBase, dicttype=OrderedDict)


# a unique id for every new member instance, to make them orderable,
# assigned and incremented in member.__init__
_memberid = 0


class member(with_metaclass(meta, typed.base)):
    """
    Base class for defining MODELED members in :class:`modeled.object`
    definitions.
    """
    strict = False

    def __init__(self, **options):
        """
        Creates a new MODELED member with the given `options`.
        """
        # the unique member ordering id
        global _memberid
        self._id = _memberid
        _memberid += 1
        # If no explicit name is given, the associated class attribute name
        # will be used and assigned in modeled.object.type.__init__:
        self.name = options.pop('name', None)
        self.title = options.pop('title', None)
        self.options = Options.frozen(options)


class InstanceMembersDictBase(simpledict.base):
    def __call__(self, mapping=None, **membervalues):
        return context(self, mapping, **membervalues)


InstanceMembersDict = simpledict('InstanceMembersDict',
  base=InstanceMembersDictBase, dicttype=OrderedDict)


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
        "getmodeledmembers() arg must be a subclass or instance "
        "of modeled.object")
