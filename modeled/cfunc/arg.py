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

__all__ = [
  'CFuncArgError', 'ArgsDict', 'arg',
  'ismodeledcfuncarg', 'getmodeledcfuncargs']

from collections import OrderedDict
from ctypes import _Pointer

from moretools import cached, simpledict, SimpleDictStructType

import modeled
from modeled.member import MemberError, member


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


class CFuncArgError(MemberError):
    __module__ = 'modeled'


DEFAULT_MTYPES = {
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
    """Metaclass for :class:`modeled.cfunc.arg`.

    - Provides modeled.cfunc.arg[<ctype>, <mtype>] initialization syntax.
    """
    __module__ = 'modeled'

    error = CFuncArgError

    @cached
    def __getitem__(cls, ctype_and_mtype):
        """Instantiate a modeled.cfunc.arg
           with given `ctype` and optional explicit `mtype`.

        - A POINTER's `mtype` maps the dereferenced type.
        - If `mtype` is omitted,
          it is taken from `modeled.cfunc.arg.DEFAULT_TYPES`,
          based on `ctype._type_`.
        """
        try:
            _ctype, mtype = ctype_and_mtype
        except TypeError:
            _ctype = ctype_and_mtype
            if issubclass(_ctype, _Pointer):
                mtype = DEFAULT_MTYPES[_ctype._type_._type_]
            else:
                mtype = DEFAULT_MTYPES[_ctype._type_]

        class typedcls(cls):
            ctype = _ctype

        return member.type.__getitem__(cls, mtype, typedcls)

Type.__name__ = 'cfunc.arg.type'


class arg(with_metaclass(Type, member)):
    """Typed function arg member of a :class:`modeled.cfunc`.
    """
    __module__ = 'modeled'

    ## def __init__(self, ctype, type_or_value, **options):
    ##     self.ctype = ctype
    ##     member.__init__(self, type_or_value, **options)

    def __repr__(self):
        return 'modeled.cfunc.arg[%s, %s]' % (
          self.ctype.__name__, self.mtype.__name__)

arg.__name__ = 'cfunc.arg'


def ismodeledcfuncarg(obj):
    """Checks if `obj` is an instance of :class:`modeled.cfunc.arg`.
    """
    return isinstance(obj, arg)


def getmodeledcfuncargs(obj):
    """Get a list of all :class:`modeled.cfunc.arg` (name, instance) pairs
       of a :class:`modeleled.cfunc` subclass
       or (name, value) pairs of a :class:`modeled.cfunc` instance
       in arg creation and inheritance order.
    """
    if modeled.ismodeledcfuncclass(obj):
        return list(obj.model.args)
    if modeled.ismodeledcfunc(obj):
        return [(name, getattr(obj, name)) for (name, _) in obj.model.args]
    raise TypeError(
      "getmodeledcfuncargs() arg must be a subclass or instance"
      " of modeled.cfunc")
