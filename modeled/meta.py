# python-modeled
#
# Copyright (C) 2014-2015 Stefan Zimmermann <zimmermann.code@gmail.com>
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

:class:`modeled.object`'s metaclass
and tools to define metaclass features on modeled class level.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from itertools import chain

from moretools import cached, qualname, dictitems

from .base import metabase as base
from .model import Model
from .member import ismodeledmemberclass, ismodeledmember
from .extension import ExtensionDeco

__all__ = [
    'meta', 'metamethod', 'metaclassmethod',
    'ismetamethod', 'ismetaclassmethod',
    'ismodeledmetaclass',
]


class meta(base):
    """Meta class for :class:`modeled.object`.
    """
    __module__ = 'modeled'

    model = Model # The basic model info metaclass

    def __new__(mcs, clsname=None, bases=None, clsattrs=None, **kwargs):
        metaattrs = {'__module__': clsattrs.get('__module__')}
        for name, obj in list(dictitems(clsattrs)):
            if ismetamethod(obj):
                metaattrs[name] = clsattrs.pop(name).func
            elif ismetaclassmethod(obj):
                metaattrs[name] = classmethod(clsattrs.pop(name).func)

        metabases = tuple(type(b) for b in bases if issubclass(b, object))
        # is this `mcs` already under the bases' metaclasses?
        if not any(issubclass(mb, mcs) for mb in metabases):
            # no? ==> change that
            metabases = (mcs, ) + metabases
        # is there a user-defined inner `meta` options class?
        meta = clsattrs.pop('meta', None)
        if meta:
            # then prepend it as additional metaclass base
            metabases = (meta, ) + metabases
        # and now create the new metaclass for the new modeled class
        mcs = type(clsname + '.meta', metabases, metaattrs)

        # create basic modeled-class-specific exception class
        mcs.Exception = type('%s.Exception' % clsname, (Exception, ), {})

        # delegate actual class creation to modeled.base.metabase
        cls = base.__new__(mcs, clsname, bases, clsattrs)
        if meta:
            # re-add user-defined inner meta options class
            # for later use in derived __new__ or __init__ methods
            clsattrs['meta'] = meta
        return cls

    def __init__(cls, clsname, bases, clsattrs):
        """Finish a :class:`modeled.object`-derived `cls`.

        - Assigns the implicit names to :class:`modeled.member` instances.
        - Creates the actual ``cls.model`` info class.
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
        model = cls.meta.model # The modeled class' model metaclass
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
        basenames = ', '.join(qualname(b) for b in bases)
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
            errclass = type(
                errclass.__name__, (errclass, cls.Exception), {})
        errclass.__qualname__ = '%s.%s' % (cls.__name__, errclass.__name__)
        setattr(type(cls), errname, errclass)
        return errclass

    @property
    def __abstractmethods__(cls):
        """Get the names of all abstract methods of this `cls`.

        - Classes with abstract methods may not be instantiated directly.
        """
        def abcnames():
            """Generator.
            """
            # don't just iterate dir(cls) as it might contain dynamic members,
            # which maybe involve cls instantiation on getattr(),
            # which leads to endless recursion.
            # and anyway: abstractmethods should always be explicitly defined!
            for name in set(chain(dir(type(cls)),
                                  *(c.__dict__ for c in cls.mro()))):
                if name == '__abstractmethods__':
                    # another way to avoid recursion :)
                    continue
                obj = getattr(cls, name, None)
                if obj is None:
                    continue
                if getattr(obj, '__isabstractmethod__', False) is True:
                    yield name

        return tuple(abcnames())

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


class metamethod(object):
    """Decorator for methods of modeled classes.
    """
    def __init__(self, func):
        """Move method `func` from modeled class to metaclass level.
        """
        self.func = func


class metaclassmethod(object):
    """Decorator for classmethods of modeled classes.
    """
    def __init__(self, func):
        """Move classmethod `func` from modeled class to metaclass level.
        """
        self.func = func


def ismetamethod(obj):
    """Check if `obj` is a ``@modeled.metamethod`` instance.
    """
    return isinstance(obj, metamethod)


def ismetaclassmethod(obj):
    """Check if `obj` is a ``@modeled.metaclassmethod`` instance.
    """
    return isinstance(obj, metaclassmethod)


def ismodeledmetaclass(mcs):
    """Checks if `mcs` is a subclass of :class:`modeled.meta`.
    """
    if not isclass(mcs):
        return False
    return issubclass(mcs, meta)
