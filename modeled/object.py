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

"""modeled.object

Provides the modeled.object base class.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['object', 'ismodeledclass', 'ismodeledobject']

from inspect import isclass

from moretools import cached, qualname

from .model import Model
from .member import ismodeledmemberclass, ismodeledmember, instancemember
from .meta import ismetamethod, ismetaclassmethod
from .base import base
from .extension import ExtensionDeco


class Type(base.type):
    """Meta class for :class:`modeled.object`.
    """
    __module__ = 'modeled'

    model = Model # The basic model info metaclass

    def __new__(mcs, clsname=None, bases=None, clsattrs=None, **kwargs):
        metaattrs = {}
        for name, obj in list(clsattrs.items()):
            if ismetamethod(obj):
                metaattrs[name] = clsattrs.pop(name).func
            elif ismetaclassmethod(obj):
                metaattrs[name] = classmethod(clsattrs.pop(name).func)
        # try:
        #     meta = clsattrs.pop('meta')
        # except KeyError:
        #     metabases = (mcs,)
        # else:
        #     metabases = (meta, mcs)
        metabases = tuple(type(b) for b in bases if issubclass(b, object))
                          ## if type(b) is not mcs)
        if not any(issubclass(mb, mcs) for mb in metabases):
            metabases = (mcs, ) + metabases
        meta = clsattrs.pop('meta', None)
        if meta:
            metabases = (meta, ) + metabases
        ## if metaattrs: # Implicitly derive a new metaclass:
        mcs = type(clsname + '.type', metabases, metaattrs)

        mcs.Exception = type('%s.Exception' % clsname, (Exception, ), {})

        cls = base.type.__new__(mcs, clsname, bases, clsattrs)
        if meta:
            clsattrs['meta'] = meta
        return cls

    def __init__(cls, clsname, bases, clsattrs):
        """Finish a :class:`modeled.object`-derived `cls`.

        - Assigns the implicit names to :class:`modeled.member`s.
        - Creates the actual `cls.model` info class.
        """
        def members():
            for name, obj in clsattrs.items():
                if ismodeledmemberclass(obj):
                    obj = obj()
                    obj.name = name
                    setattr(cls, name, obj)
                    yield obj
                elif ismodeledmember(obj):
                    if not obj.name:
                        obj.name = name
                    # also explicitly assign
                    #  (was maybe only added to clsattrs dict
                    #   by some derived metaclass)
                    setattr(cls, name, obj)
                    yield obj

        options = clsattrs.get('model') # The user-defined model options
        model = cls.type.model # The modeled object type's model metaclass
        cls.model = model(mclass=cls, members=members(), options=options)

    @cached
    def __getitem__(cls, bases):
        """Get a modeled class derived from the given `bases`,
           which can be (mixed) modeled and non-modeled classes.

        - Results are cached.
        - Needed in Python 3 for deriving from more than one modeled class:

        .. code:: python

            class Derived(ModeledBaseOne, ModeledBaseTwo):
                # results in metaclass conflict!

            class Derived(modeled.object[ModeledBaseOne, ModeledBaseTwo]):
                # works!
                ...
        """
        mcs = type(cls)
        if not isinstance(bases, tuple):
            bases = bases,
        basenames = ', '.join(map(qualname, bases))
        clsname = '%s[%s]' % (cls.__name__, basenames)
        metabases = tuple(type(b) for b in bases if issubclass(b, object))
                          ## if type(b) is not mcs)
        if not any(issubclass(mb, mcs) for mb in metabases):
            metabases = (mcs, ) + metabases
        if not any(issubclass(b, cls) for b in bases):
            bases = (cls, ) + bases
        clsattrs = {'__module__': cls.__module__}
        meta = type(clsname + '.meta', metabases, clsattrs)
        cls = meta(clsname, bases, clsattrs)
        cls.__qualname__ = '%s[%s]' % (qualname(cls), basenames)
        meta.__qualname__ = cls.__qualname__ + '.meta'
        return cls

    @property
    @cached
    def extension(cls):
        return ExtensionDeco(cls)

    def exception(cls, errclass):
        errname = errclass.__name__
        # create subclass with cls.Exception base if not based yet
        if not issubclass(errclass, cls.Exception):
            errclass = type(errclass.__name__,
              (errclass, cls.Exception), {})
        errclass.__qualname__ = '%s.%s' % (cls.__name__, errclass.__name__)
        setattr(type(cls), errname, errclass)
        return errclass

    @classmethod
    def metaclassmethod(mcs, func):
        setattr(mcs, func.__name__, classmethod(func))
        return func

    @classmethod
    def metamethod(mcs, func):
        setattr(mcs, func.__name__, func)
        return func

    @classmethod
    def metaproperty(mcs, func):
        setattr(mcs, func.__name__, property(func))
        return func

    def classmethod(cls, func):
        setattr(cls, func.__name__, classmethod(func))
        return func

    def method(cls, func):
        setattr(cls, func.__name__, func)
        return func

    def property(cls, func):
        setattr(cls, func.__name__, property(func))
        return func

Type.__name__ = 'object.type'


class object(with_metaclass(Type, base)):
    """Base class for modeled classes.
    """
    __module__ = 'modeled'

    def __new__(cls, *args, **kwargs):
        self = base.__new__(cls)
        self.model = self.model(minstance=self)
        return self

    def __init__(self, **membervalues):
        for name, value in membervalues.items():
            self.m[name].value = value

        extclasses = []
        for extclass, extdeco in self.model.extensions.items():
            if extdeco.check(self):
                extclasses.append(extclass)
                for name, m in extclass.model.members:
                    self.m[name] = self.__dict__[name] \
                      = instancemember(m, self)
        if extclasses:
            meta = type('meta', tuple(ext.meta for ext in extclasses), {})
            self.__class__ = type(self).type(self.model.name,
              tuple(extclasses) + (type(self), ), {
                '__module__': type(self).__module__,
                'meta': meta,
                })

    @property
    def m(self):
        """Access instancemember objects via self.m.<member>
        """
        return self.model.members


def ismodeledclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.object`.
    """
    if not isclass(cls):
        return False
    return issubclass(cls, object)


def ismodeledobject(obj):
    """Checks if `obj` is an instance
       of :class:`modeled.object` (or a derived class).
    """
    return isinstance(obj, object)
