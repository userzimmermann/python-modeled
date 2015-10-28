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

from moretools import cached, decamelize

import modeled
from . import member


class meta(member.type):
    @cached
    def __getitem__(cls, mtype):
        return member.type.__getitem__(cls, modeled.list[mtype])

    @property
    def itemtype(cls):
        return cls.mtype.mtype

meta.__name__ = 'member.list.meta'


class List(with_metaclass(meta, member)):
    __module__ = 'modeled'

    @property
    def itemtype(self):
        return self.mtype.mtype

    def __init__(self, items=None, **options):
        if items is None:
            items = []
        try:
            assert(issubclass(self.mtype, modeled.list))
        except AttributeError:
            items = modeled.list(items)
            self.__class__ = type(self)[items.mtype]
        member.__init__(self, items, **options)
        self.indexname = options.get('indexname', 'index')
        try:
            self.itemname = options['itemname']
        except KeyError:
            if modeled.ismodeledclass(self.itemtype):
                self.itemname = decamelize(self.itemtype.__name__)
            else:
                self.itemname = 'item'

List.__name__ = 'member.list'
