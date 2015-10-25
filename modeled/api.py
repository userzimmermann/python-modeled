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

from .typed import typed

from .cfunc import (
    cfunc, ismodeledcfuncclass, ismodeledcfuncresult,
    CFuncArgError, ismodeledcfuncarg, getmodeledcfuncargs,
)
mcfunc = cfunc
mcarg = cfunc.arg

from .adapter import Adapter, meta as AdapterMeta
