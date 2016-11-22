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

"""modeled.data.dict

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

from moretools import cached, decamelize

import modeled

from . import data


class meta(data.meta):
    __qualname__ = 'data.dict.meta'

    @cached
    def __getitem__(cls, keytype_and_valuetype):
        return super(meta, cls).__getitem__(
            modeled.dict[keytype_and_valuetype])

    @property
    def itemtype(cls):
        """
        >>> modeled.data.dict[str, int].itemtype
        <class 'modeled.tuple[str, int]'>
        """
        return cls.type.type

    @property
    def keytype(cls):
        """
        >>> modeled.data.dict[str, int].keytype
        <class 'str'>
        """
        return cls.type.type.mtypes[0]

    @property
    def valuetype(cls):
        """
        >>> modeled.data.dict[str, int]().valuetype
        <class 'int'>
        """
        return cls.type.type.mtypes[1]



class dict(data, metaclass=meta):
    __qualname__ = 'data.dict'

    @property
    def itemtype(self):
        """
        >>> modeled.data.dict[str, int]().itemtype
        <class 'modeled.tuple[str, int]'>
        """
        return self.type.itemtype

    @property
    def keytype(self):
        """
        >>> modeled.data.dict[str, int]().keytype
        <class 'str'>
        """
        return self.type.keytype

    @property
    def valuetype(self):
        """
        >>> modeled.data.dict[str, int]().valuetype
        <class 'int'>
        """
        return self.type.valuetype

    def __init__(self, items=None, **options):
        if items is None:
            items = {}
        try:
            assert issubclass(self.type, modeled.dict)
        except AttributeError:
            # ==> no data type defined
            # ==> let modeled.dict determine keytype and valuetype
            items = modeled.dict(items)
            # and derive a typed Dict based on the determined types
            self.__class__ = type(self)[items.itemtype]
        data.__init__(self, items, **options)
        self.keyname = options.get('keyname', 'key')
        try:
            self.valuename = options['valuename']
        except KeyError:
            if modeled.ismodeledclass(self.valuetype):
                self.valuename = decamelize(self.valuetype.__name__)
            else:
                self.valuename = 'value'
