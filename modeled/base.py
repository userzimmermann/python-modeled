# python-modeled
#
# Copyright (C) 2014-2015 Stefan Zimmermann <zimmermann.code@gmail.com>
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

Base class and metaclass for all modeled components.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass
from warnings import warn
from itertools import chain

import zetup

__all__ = ['metabase', 'base']


class metabase(zetup.meta):
    """Base metaclass for all :mod:`modeled` components.
    """
    @property
    def meta(cls):
        """Get the metaclass (type) of `cls`.
        """
        return type(cls)

    @property
    def type(cls):
        """Get the metaclass (type) of `cls`.
        """
        warn("'%s.type' property is deprecated. Use '%s.meta' instead."
             % (cls, cls), DeprecationWarning)
        return cls.meta

    @classmethod
    def metamro(mcs):
        """Get method resolution order of metaclass.
        """
        return mcs.mro(mcs)


class base(with_metaclass(metabase, zetup.object)):
    """Base class for all :mod:`modeled` components.
    """
