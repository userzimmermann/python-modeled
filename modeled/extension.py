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

"""modeled.extension

Provides the modeled.object.extension base class.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['ExtensionDeco']


class ExtensionDeco(object):
    def __init__(self, mclass):
        self.mclass = mclass
        self.m = Members(mclass)

    def check(self, minstance):
        raise NotImplementedError


class Members(ExtensionDeco):
    def __init__(self, mclass, **mvalues):
        self.mclass = mclass
        self.mvalues = mvalues

    def __call__(self, extclass=None, **mvalues):
        mvalues = dict(self.mvalues, **mvalues)
        extdeco = Members(self.mclass, **mvalues)
        if extclass is not None:
            self.mclass.model.extensions[extclass] = extdeco
            return extclass
        return extdeco

    def __getattr__(self, mname):
        return MemberName(self.mclass, mname)

    def check(self, minstance):
        for name, value in self.mvalues.items():
            if getattr(minstance, name) != value:
                return False
        return True


class MemberName(Members):
    def __init__(self, mclass, mname):
        Members.__init__(self, mclass)
        self.mname = mname

    def __call__(self, extclass):
        mvalues = {self.mname: extclass.__name__}
        return Members.__call__(self, extclass, **mvalues)
