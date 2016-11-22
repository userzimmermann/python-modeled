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

"""modeled.data.tuple

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

from moretools import cached

import modeled

from . import data


class meta(data.meta):
    """
    Metaclass for :class:`modeled.data`.
    """
    __qualname__ = 'data.tuple.meta'

    @cached
    def __getitem__(cls, types):
        return super(meta, cls).__getitem__(modeled.tuple[types])


class tuple(data, metaclass=meta):
    __qualname__ = 'data.tuple'

    def __init__(self, items=None, **options):
        try:
            assert(issubclass(self.type, modeled.tuple))
        except AttributeError:
            items = modeled.tuple(items)
            self.__class__ = type(self)[items.mtypes]
            data.__init__(self, items, **options)
        else:
            if items is None:
                data.__init__(self, **options)
            else:
                data.__init__(self, items, **options)
