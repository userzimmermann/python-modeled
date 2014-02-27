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

"""modeled.cfunc.arg

Provides a special modeled.member class for modeled.cfunc.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['ArgsDict', 'arg', 'ismodeledcfuncarg']

from collections import OrderedDict
from ctypes import _Pointer

from moretools import simpledict, SimpleDictStructType

import modeled
from modeled.member import member


class ArgsDictStructType(SimpleDictStructType):
    """`basestructtype` for `simpledict()` to create ArgsDict.struct class.
    """
    def __init__(self, model, args):
        def bases():
            for cls in model.__bases__:
                if cls is not modeled.object.model:
                    yield cls.args
        # Delegates args to SimpleDictType.__init__()
        SimpleDictStructType.__init__( # First arg is struct __name__
          self, '%s.args' % repr(model), bases(), args)


ArgsDict = simpledict(
  'ArgsDict', basestructtype=ArgsDictStructType,
  dicttype=OrderedDict)


DEFAULT_DTYPES = {
  'i': int,
  'I': int,
  'l': int,
  'L': int,
  'f': float,
  'd': float,
  'P': int,
  'z': bytes,
  }


class Type(member.type):
    __module__ = 'modeled'

    def __getitem__(cls, ctype_and_dtype):
        try:
            ctype, dtype = ctype_and_dtype
        except TypeError:
            ctype = ctype_and_dtype
            if issubclass(ctype, _Pointer):
                dtype = DEFAULT_DTYPES[ctype._type_._type_]
            else:
                dtype = DEFAULT_DTYPES[ctype._type_]

        return cls(ctype, dtype)

Type.__name__ = 'cfunc.arg.type'


class arg(with_metaclass(Type, member)):
    __module__ = 'modeled'

    def __init__(self, ctype, type_or_value, **options):
        self.ctype = ctype
        member.__init__(self, type_or_value, **options)

    def __repr__(self):
        return 'modeled.cfunc.arg[%s, %s]' % (
          self.ctype.__name__, self.dtype.__name__)

arg.__name__ = 'cfunc.arg'


def ismodeledcfuncarg(obj):
    """Checks if `obj` is an instance of :class:`modeled.cfunc.arg`.
    """
    return isinstance(obj, arg)
