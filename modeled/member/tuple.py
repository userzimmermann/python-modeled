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

"""modeled.member.tuple

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

from moretools import cached

from modeled import mtuple
from . import member


class Type(member.type):
    __module__ = 'modeled'

    @cached
    def __getitem__(cls, mtypes):
        return member.type.__getitem__(cls, mtuple[mtypes])

Type.__name__ = 'member.tuple.type'


class Tuple(with_metaclass(Type, member)):
    __module__ = 'modeled'

    def __init__(self, items=None, **options):
        try:
            assert(issubclass(self.mtype, mtuple))
        except AttributeError:
            items = mtuple(items)
            self.__class__ = type(self)[items.mtypes]
            member.__init__(self, items, **options)
        else:
            if items is None:
                member.__init__(self, **options)
            else:
                member.__init__(self, items, **options)

Tuple.__name__ = 'member.tuple'
