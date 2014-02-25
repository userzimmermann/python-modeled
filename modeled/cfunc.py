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
__all__ = ['cfunc', 'ismodeledcfunc']

from six import add_metaclass, with_metaclass

from ctypes import _SimpleCData, _Pointer, byref

import modeled
from .member import MemberError


class Model(modeled.object.model.type):
    __module__ = 'modeled'

    def __init__(self, modeledclass, members=None, options=None):
        options = Model.options(options)
        if options:
            try:
                self.restype = options['restype']
            except KeyError:
                pass
            try:
                self.cfunc = options['cfunc']
            except KeyError:
                pass
        modeled.object.model.type.__init__(
          self, modeledclass, members, options)

Model.__name__ = 'cfunc.model.type'


class Type(modeled.object.type):
    __module__ = 'modeled'

    model = Model

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


DEFAULT_DTYPES = {
  'i': int,
  'I': int,
  'l': int,
  'L': int,
  'f': float,
  'd': float,
  ## 'P': Hex,
  'z': bytes,
  }


class cfunc(with_metaclass(Type, modeled.object)):
    def __init__(self, *args, **kwargs):
        for arg, (name, _) in zip(args, self.model.members):
            kwargs[name] = arg
        modeled.object.__init__(self, **kwargs)

        cfunc = self.model.cfunc
        args = []
        for (name, _), argtype in zip(self.model.members, cfunc.argtypes):
            try:
                value = kwargs[name]
            except KeyError:
                try:
                    value = getattr(self, name)
                except MemberError:
                    pass
            if issubclass(argtype, _Pointer):
                try:
                    cvalue = argtype._type_(value)
                except NameError: # No value
                    cvalue = argtype._type_()
                arg = byref(cvalue)
            else:
                arg = argtype(value)
            args.append(arg)
        res = self.model.cfunc(*args)
        if self.model.restype:
            return self.model.restype(res)
        return res


def ismodeledcfunc(obj):
    """Checks if `obj` is an instance
       of :class:`modeled.cfunc` (or a derived class).
    """
    return isinstance(obj, cfunc)
