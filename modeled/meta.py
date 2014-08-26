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

"""modeled.meta

Define metaclass features on modeled class definition level.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = [
  'metamethod', 'ismetamethod',
  'metaclassmethod', 'ismetaclassmethod',
  ]


class metamethod(object):
    def __init__(self, func):
        self.func = func


class metaclassmethod(object):
    def __init__(self, func):
        self.func = func


def ismetamethod(obj):
    return isinstance(obj, metamethod)


def ismetaclassmethod(obj):
    return isinstance(obj, metaclassmethod)
