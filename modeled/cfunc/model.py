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

"""modeled.cfunc.model

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['Model']

from modeled.object import object as mobject

from .arg import ArgsDict, ismodeledcfuncarg


class Model(mobject.model.meta):
    """Metaclass for :class:`modeled.cfunc.model`.

    - Checks user-defined `class model` for `restype` and `cfunc` options.
    """
    __module__ = 'modeled.cfunc'
    __qualname__ = 'cfunc.model.meta'

    def __init__(cls, owner, members=None, options=None):
        options = Model.options(options)
        super(Model, cls).__init__(owner, members, options)
        cls.args = ArgsDict.struct(model=cls, args=(
            (name, arg) for name, arg in cls.members
            if ismodeledcfuncarg(arg)))
        if options: # No restype or cfunc option ==> undefined
            # (Will be inherited from base model class
            #  or cause AttributeError on access)
            try:
                cls.restype = options['restype']
            except KeyError:
                pass
            try:
                cls.cfunc = options['cfunc']
            except KeyError:
                pass
