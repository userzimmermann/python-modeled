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

"""modeled.list

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['list']

from six.moves import builtins

from . import typed


class list(typed.base, builtins.list):
    __module__ = 'modeled'

    def __init__(self, iterable):
        items = iter(iterable)
        try:
            self.mtype
        except AttributeError:
            try:
                first = next(items)
            except StopIteration:
                raise TypeError
            self.__class__ = type(self)[type(first)]
            self.append(first)
        self.extend(items)

    def append(self, item):
        if not isinstance(item, self.mtype):
            item = self.mtype(item)
        builtins.list.append(self, item)

    def extend(self, iterable):
        def items():
            for item in iterable:
                if not isinstance(item, self.mtype):
                    yield self.mtype(item)
                else:
                    yield item

        builtins.list.extend(self, items())
