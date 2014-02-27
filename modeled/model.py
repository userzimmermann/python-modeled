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

from six import PY3, add_metaclass, with_metaclass

from inspect import isclass, getmembers

import modeled
from .options import Options
from .member import MembersDict, getmodeledmembers
from .property import PropertiesDict, ismodeledproperty


def _options(options):
    if not options:
        return None
    if not isinstance(options, dict):
        return dict(getmembers(options))
    return options


class Model(type):
    """Model info metaclass for creating :class:`modeled.object`.

    - Provides access to all :class:`modeled.member` definitions
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

    def __new__(mcs, modeledclass, members=None, options=None):
        def bases():
            for cls in modeledclass.__bases__:
                try:
                    yield cls.model
                except AttributeError:
                    pass

        return type.__new__(
          mcs, '%s.model' % modeledclass.__name__, tuple(bases()), {
            '__module__': modeledclass.__module__,
            })

    def __init__(self, modeledclass, members=None, options=None):
        """Create the model info for `modeledclass`
           with optional override `members` and `options`.
        """
        self.modeledclass = modeledclass
        print self, modeledclass, members, options
        ## try:
        ##     options = options or modeledclass.model
        ## except AttributeError: # No options.
        options = _options(options)
        ## options = model.options(options)
        if not options:
            self.name = modeledclass.__name__
            self.options = Options.struct(model=self)
        else:
            ## if not isinstance(options, dict):
            ##     options = dict(getmembers(options))
            self.name = options.pop('name', modeledclass.__name__)
            self.options = Options.struct(model=self, options=options)
        if members:
            self.members = MembersDict.struct(model=self, members=(
              (m.name, m) for m in sorted(members, key=lambda m: m._id)))
            ## self.members = memberstype(modeledclass,
            ##   ((m.name, m) for m in sorted(members, key=lambda m: m._id)))
        else:
            self.members = MembersDict.struct(
              model=self, members=getmodeledmembers(modeledclass))
            ## self.members = memberstype(modeledclass, getmodeledmembers(modeledclass))
        self.properties = PropertiesDict.struct(model=self, properties=(
          (name, m) for name, m in self.members if ismodeledproperty(m)))

    def __repr__(self):
        return '%s.model' % self.modeledclass.__name__

    @property
    def type(cls):
        """Get a :class:`model`'s meta class with .type.
        """
        return type(cls)

Model.__name__ = 'object.type.model'
