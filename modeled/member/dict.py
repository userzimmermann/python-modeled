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

"""modeled.member.dict

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

from moretools import cached, decamelize

import modeled
from . import member


class meta(member.meta):
    @cached
    def __getitem__(cls, mtypes):
        return member.type.__getitem__(cls, modeled.dict[mtypes])

    @property
    def itemtype(cls):
        return cls.mtype.mtype

    @property
    def keytype(cls):
        return cls.mtype.mtype.mtypes[0]

    @property
    def valuetype(cls):
        return cls.mtype.mtype.mtypes[1]

meta.__name__ = 'member.dict.meta'


class Dict(with_metaclass(meta, member)):
    __module__ = 'modeled'

    @property
    def itemtype(self):
        return self.mtype.mtype

    @property
    def keytype(self):
        return self.mtype.mtype.mtypes[0]

    @property
    def valuetype(self):
        return self.mtype.mtype.mtypes[1]

    def __init__(self, items=None, **options):
        if items is None:
            items = {}
        try:
            assert(issubclass(self.mtype, modeled.dict))
        except AttributeError:
            items = modeled.dict(items)
            self.__class__ = type(self)[items.mtype.mtypes]
        member.__init__(self, items, **options)
        self.keyname = options.get('keyname', 'key')
        try:
            self.valuename = options['valuename']
        except KeyError:
            if modeled.ismodeledclass(self.valuetype):
                self.valuename = decamelize(self.valuetype.__name__)
            else:
                self.valuename = 'value'

Dict.__name__ = 'member.dict'
