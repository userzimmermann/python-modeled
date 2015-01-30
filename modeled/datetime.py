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

"""modeled.datetime

The modeled.datetime (mdatetime) class.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from __future__ import absolute_import
from six import with_metaclass

__all__ = ['datetime']

from datetime import datetime as base

from moretools import isstring


class Meta(type(base)):
    """Metaclass for :class:`modeled.datetime`.
    """
    def __getitem__(cls, format):
        class subclass(cls):
            pass

        subclass.format = format = str(format)
        subclass.__name__ = subclass.__qualname__ = '%s[%s]' % (
          cls.__name__, repr(format))


class datetime(with_metaclass(Meta, base)):
    """modeled.datetime, a :class:`datetime.datetime`-derived class
       with these additional features:

    - Class-bound <datetime class>.format string
      for converting to and from string representation,
      which defaults to '%Y-%m-%d %H:%M:%S'
      and can be customized by creating subclasses
      via modeled.datetime[<format string>]
    - Supports direct instantiation from single string arg,
      implicitly using the class-bound format for parsing.
    """
    format = '%Y-%m-%d %H:%M:%S'

    def __new__(cls, string_or_year, *mdhms):
        """Create a new :class:`modeled.datetime` instance
           by giving either a 
        """
        if isstring(string_or_year):
            dt = base.strptime(string_or_year, cls.format)
            return base.__new__(cls, *dt.timetuple()[:6])

        return base.__new__(cls, string_or_year, *mdhms)
