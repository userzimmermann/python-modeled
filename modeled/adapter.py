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

"""modeled.adapter

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass

__all__ = ['Adapter']

from moretools import cached

from modeled import ismodeledclass, ismodeledobject
from .base import base


class Type(base.type):
    __module__ = 'modeled'

    @cached
    def __getitem__(cls, mclass):
        if not ismodeledclass(mclass):
            raise TypeError

        class Type(type(cls), type(mclass)):
            pass

        Type.__name__ = '%s[%s].type' % (cls.__name__, mclass.__name__)

        class Adapter(with_metaclass(Type, cls, mclass)):
            # Reset __new__ from base Adapter.__new__
            # (adapting modeled instances)
            # to <adapted modeled class>.__new__ (instantiating class)
            __new__ = mclass.__new__

            def __init__(self, *args, **membervalues):
                # first delegate to __init__ of adapted modeled class
                mclass.__init__(self, *args, **membervalues)
                self.minstance = self
                # and then to adapter's additional __init__
                cls.__init__(self)

        Adapter.mclass = mclass
        Adapter.__module__ = cls.__module__
        Adapter.__name__ = '%s[%s]' % (cls.__name__, mclass.__name__)
        return Adapter

Type.__name__ = 'Adapter.type'


class Adapter(with_metaclass(Type, base)):
    __module__ = 'modeled'

    def __new__(cls, minstance, *args):
        class Adapter(cls):
            def __init__(self, minstance, *args):
                if not ismodeledobject(minstance):
                    raise TypeError
                self.minstance = minstance
                self.model = minstance.model
                ## cls.__init__(self, *args)

        return base.__new__(Adapter)
