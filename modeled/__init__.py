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

"""modeled

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

import zetup

zetup.annotate(__name__)

import sys

from path import Path


for path in (Path(p) / 'modeled' for p in sys.path):
    if path.isdir():
        __path__.append(path.realpath())


from .base import *

from .tuple import *
mtuple = tuple
ismtupleclass = ismodeledtupleclass
ismtuple = ismodeledtuple

from .list import *
mlist = list
ismlistclass = ismodeledlistclass
ismlist = ismodeledlist

from .dict import *
mdict = dict
ismdictclass = ismodeleddictclass
ismdict = ismodeleddict

from .range import *
mrange = range

from .datetime import *
mdatetime = datetime

from .namedtuple import *

from .simpledict import *

from .options import *

from .meta import *

from .object import *
M = mobject = object

from .member import *
m = member

from .property import *
mproperty = property

from .typed import typed

from .cfunc import *
mcfunc = cfunc
mcarg = cfunc.arg

from .adapter import *
