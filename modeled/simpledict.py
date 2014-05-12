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

"""modeled.simpledict

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['simpledict']

import sys

import moretools
from moretools import cached

from modeled import mtuple, mdict
from . import typed


def simpledict(typename, **kwargs):
    basedict = moretools.simpledict(typename, **kwargs)

    class Type(mdict.type, type(basedict)):
        @cached
        def __getitem__(cls, mtypes):
            class Type(type(cls)):
                mtype = mtuple[mtypes]
                mkeytype = mtype.mtypes[0]
                mvaluetype = mtype.mtypes[1]

            Type.__module__ = cls.__module__
            Type.__name__ = '%s.type[%s, %s]' % (
              cls.__name__, Type.mkeytype.__name__, Type.mvaluetype.__name__)

            class typedcls(with_metaclass(Type, cls)):
                pass

            typedcls.__module__ = cls.__module__
            typedcls.__name__ = '%s[%s, %s]' % (
              cls.__name__, Type.mkeytype.__name__, Type.mvaluetype.__name__)
            return typedcls

    class simpledict(with_metaclass(Type, typed.base, basedict)):
        def __setitem__(self, key, value):
            cls = type(self)
            if not isinstance(key, cls.mkeytype):
                key = cls.mkeytype(key)
            if not isinstance(value, cls.mvaluetype):
                value = cls.mvaluetype(value)
            basedict.__setitem__(self, key, value)

    try: # Taken from collections.py:
        simpledict.__module__ = Type.__module__ = (
          sys._getframe(1).f_globals.get('__name__', '__main__'))
    except (AttributeError, ValueError):
        pass

    Type.__name__ = typename + '.type'
    simpledict.__name__ = typename
    return simpledict
