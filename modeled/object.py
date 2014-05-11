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

"""modeled.object

Provides the modeled.object base class.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['object', 'ismodeledclass', 'ismodeledobject']

from .model import Model
from .member import ismodeledmemberclass, ismodeledmember
from .base import base


class Type(base.type):
    """Meta class for :class:`modeled.object`.
    """
    model = Model # The basic model info metaclass

    def __init__(cls, clsname, bases, clsattrs):
        """Finish a :class:`modeled.object`-derived `cls`.

        - Assigns the implicit names to :class:`modeled.member`s.
        - Creates the actual `cls.model` info class.
        """
        def members():
            for name, obj in clsattrs.items():
                if ismodeledmemberclass(obj):
                    obj = obj()
                    obj.name = name
                    setattr(cls, name, obj)
                    yield obj
                elif ismodeledmember(obj):
                    if not obj.name:
                        obj.name = name
                    yield obj

        options = clsattrs.get('model') # The user-defined model options
        model = cls.type.model # The modeled object type's model metaclass
        cls.model = model(mclass=cls, members=members(), options=options)


class object(with_metaclass(Type, base)):
    """Base class for modeled classes.
    """
    __module__ = 'modeled'

    def __init__(self, **membervalues):
        for name, value in membervalues.items():
            setattr(self, name, value)


def ismodeledclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.object`.
    """
    try:
        return issubclass(cls, object)
    except TypeError: # No class at all
        return False


def ismodeledobject(obj):
    """Checks if `obj` is an instance
       of :class:`modeled.object` (or a derived class).
    """
    return isinstance(obj, object)
