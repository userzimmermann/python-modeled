# python-modeled
#
# Copyright (C) 2014-2016 Stefan Zimmermann <zimmermann.code@gmail.com>
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

"""modeled

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__import__('zetup').toplevel(__name__, [
    'base',
    'tuple', 'list', 'dict',
    'range', 'datetime', 'namedtuple', 'simpledict',
    'options', 'Options'
    'meta', 'metamethod', 'metaclassmethod',
    'ismetamethod', 'ismetaclassmethod', # 'ismodeledmetaclass',
    'object', 'ismodeledclass', 'ismodeledobject',
    'MembersDict', 'MemberError', 'member',
    'InstanceMembersDict', 'instancemember',
    # 'ismodeledmemberclass', 'ismodeledmember', 'ismodeledinstancemember',
    # 'getmodeledmembers',
    'PropertyError', 'PropertiesDict', 'property',
    # 'ismodeledproperty', 'getmodeledproperties',
    'cfunc', # 'ismodeledcfuncclass', 'ismodeledcfuncresult',
    'CFuncArgError', # 'ismodeledcfuncarg', 'getmodeledcfuncargs',
    'Adapter', 'AdapterMeta',
], __call__=lambda obj: deco(obj))

import sys
from path import Path
# search sys.path for other packages using modeled namespace
for path in (Path(p) / 'modeled' for p in sys.path):
    if path.isdir():
        __path__.append(path.realpath())
del sys, path, Path


from .base import base

from .tuple import tuple, ismodeledtupleclass, ismodeledtuple
mtuple = tuple
ismtupleclass = ismodeledtupleclass
ismtuple = ismodeledtuple

from .list import list, ismodeledlistclass, ismodeledlist
mlist = list
ismlistclass = ismodeledlistclass
ismlist = ismodeledlist

from .dict import dict, ismodeleddictclass, ismodeleddict
mdict = dict
ismdictclass = ismodeleddictclass
ismdict = ismodeleddict

from .range import range
mrange = range

from .datetime import datetime
mdatetime = datetime

from .namedtuple import namedtuple

from .simpledict import simpledict

from .options import OptionError, Options

from .meta import (
    meta, metamethod, metaclassmethod, ismetamethod, ismetaclassmethod,
    ismodeledmetaclass,
)

from .object import object, ismodeledclass, ismodeledobject
M = mobject = object

from .member import (
    MembersDict, MemberError, member,
    InstanceMembersDict, instancemember,
    ismodeledmemberclass, ismodeledmember, ismodeledinstancemember,
    getmodeledmembers,
)
m = member

from .property import (
    PropertyError, PropertiesDict, property,
    ismodeledproperty, getmodeledproperties,
)
mproperty = property

from .strict import strict
from .typed import typed

from .data import data

from .cfunc import (
    cfunc, ismodeledcfuncclass, ismodeledcfuncresult,
    CFuncArgError, ismodeledcfuncarg, getmodeledcfuncargs,
)
mcfunc = cfunc
mcarg = cfunc.arg

from .adapter import Adapter, meta as AdapterMeta


from inspect import isclass, isfunction, getmembers


def deco(obj):
    """The logic behind the ``@modeled`` decorator.
    """
    if isclass(obj):
        return object[meta(
            obj.__name__, obj.__bases__, dict(getmembers(obj)))]

    if isfunction(obj):
        return typed(obj)
