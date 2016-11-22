# python-modeled
#
# Copyright (C) 2014-2016 Stefan Zimmermann <zimmermann.code@gmail.com>
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

"""modeled.member.instancemember

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from moretools import cached

from .handlers import Handlers


class instancemember(object):
    __module__ = 'modeled'

    def __init__(self, origin, owner):
        self.origin = origin
        self.owner = owner
        self.changed = Handlers()

    @property
    def name(self):
        return self.origin.name

    @property
    def title(self):
        return self.origin.title

    @property
    def value(self):
        return self.origin.__get__(self.owner)

    @value.setter
    def value(self, value):
        return self.origin.__set__(self.owner, value)

    @cached
    def __getitem__(self, key):
        return type(self)(self.origin[key], self.owner)

    def __iter__(self):
        raise TypeError("%s object is not iterable" % type(self))

    def __repr__(self):
        return "%s(%s)" % (type(self), repr(self.origin))
