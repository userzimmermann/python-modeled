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

The ``modeled.datetime`` class.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['datetime']

from moretools import isstring

import modeled


class meta(modeled.base.meta):
    """
    Metaclass for :class:`modeled.datetime`:

    * Provides ``modeled.datetime[format]`` syntax via :meth:`__getitem__`
      for creating subclasses with custom string representation format.
    * Defines :meth:`.__subclasscheck__` for making
      ``modeled.datetime[format]`` classes appear as subclasses of
      :class:`modeled.datetime`, although no directly derived.

    See `class`:modeled.datetime` for more information and examples.
    """
    __qualname__ = 'datetime.meta'

    class base(__import__('datetime').datetime, modeled.base):
        """
        Base class for :class:`modeled.datetime` and all
        ``modeled.datetime[format]`` subclasses.
        """
        __qualname__ = 'datetime.base'

        def __new__(cls, string_or_year, *mdhms):
            """
            Create a new :class:`modeled.datetime` instance by giving either a
            string representation:

            >>> modeled.datetime("2013-12-11 10:09:08")
            datetime(2013, 12, 11, 10, 9, 8)

            Or arguments as expected by standard ``datetime.datetime``:

            >>> modeled.datetime(2013, 12, 11, 10, 9, 8)
            datetime(2013, 12, 11, 10, 9, 8)
            """
            if isstring(string_or_year):
                dt = meta.base.strptime(string_or_year, cls.format)
                return meta.base.__new__(cls, *dt.timetuple()[:6])

            return super().__new__(cls, string_or_year, *mdhms)

    def __subclasscheck__(cls, subcls):
        """
        Make classes created by ``modeled.datetime[format]`` appear as
        subclasses of :class:`modeled.datetime`, although they are only
        derived from :class:
        """
        return issubclass(subcls, cls.base)

    def __getitem__(cls, _format):

        class sub(cls.base):
            format = str(_format)

        sub.__name__ = '%s[%s]' % (cls.__name__, repr(sub.format))
        sub.__qualname__ = '%s[%s]' % (cls.__qualname__, repr(sub.format))
        return sub


class datetime(meta.base, metaclass=meta):
    """
    MODELED datetime class derived from standard ``datetime.datetime``
    with some additional features:

    * Class-bound ``.format`` string for converting to and from string
      representations, which defaults to ``"%Y-%m-%d %H:%M:%S"``
      and can be customized by creating subclasses:

    >>> dtcls = modeled.datetime["%Y/%m/%d %H-%M-%S"]
    >>> dtcls
    <class 'modeled.datetime.datetime['%Y/%m/%d %H-%M-%S']'>
    >>> dtcls(2013, 12, 11, 10, 9, 8)
    datetime['%Y/%m/%d %H-%M-%S'](2013, 12, 11, 10, 9, 8)

    * Supports direct instantiation from single string arg,
      which must match the class-bound ``.format`` string:

    >>> modeled.datetime("2013-12-11 10:09:08")
    datetime(2013, 12, 11, 10, 9, 8)
    """
    # default string representation
    format = "%Y-%m-%d %H:%M:%S"
