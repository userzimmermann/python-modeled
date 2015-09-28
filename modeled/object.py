# python-modeled
#
# Copyright (C) 2014-2015 Stefan Zimmermann <zimmermann.code@gmail.com>
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

:class:`modeled.object` and related type check tools.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass
from inspect import isclass

from .member import instancemember
from .meta import meta
from .base import base

__all__ = ['object', 'ismodeledclass', 'ismodeledobject']


class object(with_metaclass(meta, base)):
    """Base class for modeled classes.
    """
    __module__ = 'modeled'

    def __new__(cls, *args, **kwargs):
        abcnames = cls.__abstractmethods__
        if abcnames:
            raise TypeError(
                "Can't instantiate abstract %s with abstract methods %s"
                % (repr(cls), ", ".join(map(repr, abcnames))))
        self = base.__new__(cls)
        self.model = self.model(minstance=self)
        return self

    def __init__(self, **membervalues):
        for name, value in membervalues.items():
            self.m[name].value = value

        extclasses = []
        for extclass, extdeco in self.model.extensions.items():
            if extdeco.check(self):
                extclasses.append(extclass)
                for name, m in extclass.model.members:
                    self.m[name] = self.__dict__[name] \
                      = instancemember(m, self)
        if extclasses:
            meta = type('meta', tuple(ext.meta for ext in extclasses), {})
            self.__class__ = type(self).type(
                self.model.name, tuple(extclasses) + (type(self), ), {
                    '__module__': type(self).__module__,
                    'meta': meta,
                })

    @property
    def m(self):
        """To access instancemember objects via ``self.m.<member name>``.
        """
        return self.model.members


def ismodeledclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.object`.
    """
    if not isclass(cls):
        return False
    return issubclass(cls, object)


def ismodeledobject(obj):
    """Checks if `obj` is an instance
       of :class:`modeled.object` (or a derived class).
    """
    return isinstance(obj, object)
