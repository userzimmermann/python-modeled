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

"""modeled.cfunc

Provides a ctypes function wrapper based on modeled.object.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = [
  'cfunc', 'ismodeledcfuncclass', 'ismodeledcfuncresult',
  # from .arg:
  'CFuncArgError', 'ismodeledcfuncarg', 'getmodeledcfuncargs']

import ctypes
from ctypes import _Pointer, byref
# Get byref type with dummy expression:
_Ref = type(byref(ctypes.c_int()))

import modeled

from .model import Model
from .arg import CFuncArgError, arg, ismodeledcfuncarg, getmodeledcfuncargs


class Type(modeled.object.type):
    """Metaclass for :class:`modeled.cfunc`.

    - Provies modeled.cfunc[<restype>, <cfunc>] syntax
      for implicitly creating modeled.cfunc derived base classes
      with .model.restype and .model.cfunc options assigned.
    """
    __module__ = 'modeled'

    model = Model # Overrides modeled.object.type.model metaclass

    arg = arg # modeled.cfunc.arg class

    def __init__(cls, clsname, bases, clsattrs):
        modeled.object.type.__init__(cls, clsname, bases, clsattrs)
        if cls.model.members:
            cls.model.cfunc.argtypes = [
              m.ctype for (name, m) in cls.model.members]

    def __getitem__(cls, restype_and_cfunc):
        try:
            restype, cfunc = restype_and_cfunc
        except TypeError:
            restype = None
            cfunc = restype_and_cfunc

        class CFunc(cls):
            model = dict(restype=restype, cfunc=cfunc)

        return CFunc

Type.__name__ = 'cfunc.type'


class cfunc(with_metaclass(Type, modeled.object)):
    """Base class for modeled.cfunc classes.

    - Instantiating means calling the associated C function.
    - Supports positional args as well as keyword args,
      based on the modeled.cfunc.arg member definitions.
    """
    def __init__(self, *args, **membervalues):
        for arg, (name, _) in zip(args, self.model.args):
            membervalues[name] = arg
        modeled.object.__init__(self, **membervalues)

        cfunc = self.model.cfunc
        args = []
        for (name, _), argtype in zip(self.model.args, cfunc.argtypes):
            try:
                value = getattr(self, name)
            except CFuncArgError as e:
                argexc = e
            if issubclass(argtype, _Pointer):
                try:
                    cvalue = argtype._type_(value)
                except NameError: # No value
                    cvalue = argtype._type_()
                arg = byref(cvalue)
            else:
                try:
                    arg = argtype(value)
                except NameError: # No value
                    raise argexc
            args.append(arg)
        self.resvalue = self.model.cfunc(*args)
        if self.model.restype:
            self.resvalue = self.model.restype(self.resvalue)
        for arg, (name, _) in zip(args, self.model.args):
            if isinstance(arg, _Ref):
                setattr(self, name, arg._obj.value)


def ismodeledcfuncclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.cfunc`.
    """
    try:
        return issubclass(cls, cfunc)
    except TypeError: # No class at all
        return False


def ismodeledcfuncresult(obj):
    """Checks if `obj` is an instance
       of :class:`modeled.cfunc` (or a derived class).
    """
    return isinstance(obj, cfunc)
