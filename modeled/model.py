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

"""modeled.model

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['Model']

from inspect import getmembers

from moretools import DictStruct, qualname

from .base import metabase


class modelbase(object):
    def __init__(self, owner):
        self.owner = owner
        self.members = InstanceMembersDict(
            (name, instancemember(origin, owner))
            for name, origin in self.members)
        owner.__dict__.update(self.members)


# Import modules that need to import modelbase in reverse:
from .options import Options
from .member import (
  MembersDict, InstanceMembersDict, instancemember, getmodeledmembers)
from .property import PropertiesDict, ismodeledproperty


def _options(options):
    if not options:
        return None
    if not isinstance(options, dict):
        return dict(getmembers(options))
    return options


class Model(metabase):
    """
    Model info metaclass for creating :class:`modeled.object`.

    * Provides access to all :class:`modeled.member` definitions
      and custom options.
    """
    __module__ = 'modeled'

    ## __slots__ = ['name', 'options', 'members', 'properties']

    @staticmethod
    def options(options):
        if not options:
            return None
        if not isinstance(options, dict):
            return dict(getmembers(options))
        return options

    def __new__(mcs, owner, members=None, options=None):
        def bases():
            for cls in owner.__bases__:
                try:
                    yield cls.model
                except AttributeError:
                    pass

        bases = tuple(bases())
        return type.__new__(
            mcs, '%s.model' % owner.__name__, bases or (modelbase, ), {
                '__module__': owner.__module__,
                'extensions': DictStruct(
                    '%s.model.extensions' % owner.__name__,
                    tuple(b.extensions for b in bases)),
            })

    def __init__(self, owner, members=None, options=None):
        """
        Create the ``.model`` holder for MODELED `owner` class
        with optional override `members` and `options`.
        """
        self.owner = owner
        ## try:
        ##     options = options or owner.model
        ## except AttributeError: # No options.
        options = _options(options)
        ## options = model.options(options)
        if not options:
            self.name = owner.__name__
            self.options = Options.struct(model=self)
        else:
            ## if not isinstance(options, dict):
            ##     options = dict(getmembers(options))
            self.name = options.pop('name', owner.__name__)
            self.options = Options.struct(model=self, options=options)
        if members:
            self.members = MembersDict.struct(model=self, members=(
              (m.name, m) for m in sorted(members, key=lambda m: m._id)))
            ## self.members = memberstype(owner,
            ##   ((m.name, m) for m in sorted(members, key=lambda m: m._id)))
        else:
            self.members = MembersDict.struct(
              model=self, members=getmodeledmembers(owner))
            ## self.members = memberstype(owner, getmodeledmembers(owner))
        self.properties = PropertiesDict.struct(model=self, properties=(
          (name, m) for name, m in self.members if ismodeledproperty(m)))
        # self.extensions = []

    def __repr__(self):
        return '%s.model' % qualname(self.owner)


Model.__name__ = 'object.meta.model'
