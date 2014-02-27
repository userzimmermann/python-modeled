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
  'cfunc', 'ismodeledcfuncclass', 'ismodeledcfunc', 'ismodeledcfuncarg']

from ctypes import _SimpleCData, _Pointer, byref

import modeled
from modeled.member import MemberError

from .arg import ArgsDict, arg, ismodeledcfuncarg


class Model(modeled.object.model.type):
    __module__ = 'modeled'

    def __init__(cls, modeledclass, members=None, options=None):
        options = Model.options(options)
        modeled.object.model.type.__init__(
          cls, modeledclass, members, options)
        cls.args = ArgsDict.struct(model=cls, args=(
          (name, a) for name, a in cls.members if ismodeledcfuncarg(a)))
        if options:
            try:
                cls.restype = options['restype']
            except KeyError:
                pass
            try:
                cls.cfunc = options['cfunc']
            except KeyError:
                pass

Model.__name__ = 'cfunc.model.type'


class Type(modeled.object.type):
    __module__ = 'modeled'

    model = Model

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
    def __init__(self, *args, **membervalues):
        for arg, (name, _) in zip(args, self.model.members):
            membervalues[name] = arg
        modeled.object.__init__(self, **membervalues)

        cfunc = self.model.cfunc
        args = []
        for (name, _), argtype in zip(self.model.members, cfunc.argtypes):
            try:
                value = getattr(self, name)
            except MemberError as e:
                membererror = e
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
                    raise membererror
            args.append(arg)
        res = self.model.cfunc(*args)
        if self.model.restype:
            return self.model.restype(res)
        return res


def ismodeledcfuncclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.cfunc`.
    """
    try:
        return issubclass(cls, cfunc)
    except TypeError: # No class at all
        return False


def ismodeledcfunc(obj):
    """Checks if `obj` is an instance
       of :class:`modeled.cfunc` (or a derived class).
    """
    return isinstance(obj, cfunc)
