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

"""modeled.member.list

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

from moretools import cached

from modeled import mlist
from . import member


class Type(member.type):
    @cached
    def __getitem__(cls, mtype):
        return member.type.__getitem__(cls, mlist[mtype])

Type.__name__ = 'member.list.type'


class List(with_metaclass(Type, member)):
    __module__ = 'modeled'

    def __init__(self, items=None, **options):
        try:
            assert(issubclass(self.mtype, mlist))
        except AttributeError:
            items = mlist(items)
            self.__class__ = type(self)[items.mtype]
            member.__init__(self, items, **options)
        else:
            if items is None:
                member.__init__(self, **options)
            else:
                member.__init__(self, items, **options)

List.__name__ = 'member.list'
