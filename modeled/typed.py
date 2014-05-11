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

"""modeled.typed

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['base']

from moretools import cached

from .base import base


class Type(base.type):
    """Base metaclass for :mod:`modeled` components
       with a connected data type (mtype).

    - Provides class[<mtype>] syntax.
    """
    @cached
    def __getitem__(cls, mtype, typedcls=None):
        """Derive a typed subclass from `cls` with given `mtype`.

        - Optionally takes a predefined `typedcls`
          from a derived metaclass.__getitem__.
        """
        if not typedcls:
            class typedcls(cls):
                pass

        typedcls.mtype = mtype
        typedcls.__module__ = cls.__module__
        typedcls.__name__ = '%s[%s]' % (cls.__name__, mtype.__name__)
        return typedcls

Type.__name__ = 'base.type'


class base(with_metaclass(Type, base)):
    pass