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

"""modeled.base

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['base']


class Type(type):
    """Base metaclass for all :mod:`modeled` components.
    """
    __module__ = 'modeled'

    @property
    def type(cls):
        """Get the metaclass of `cls` with `.type`.
        """
        return type(cls)

    meta = type

Type.__name__ = 'base.type'


class base(with_metaclass(Type, object)):
    """Base class for all :mod:`modeled` components.
    """
    __module__ = 'modeled'
