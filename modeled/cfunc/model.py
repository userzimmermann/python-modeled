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

import modeled

from .arg import ArgsDict, ismodeledcfuncarg


class Model(modeled.object.model.type):
    """Metaclass for :class:`modeled.cfunc.model`.

    - Checks user-defined `class model` for `restype` and `cfunc` options.
    """
    __module__ = 'modeled'

    def __init__(cls, mclass, members=None, options=None):
        options = Model.options(options)
        modeled.object.model.type.__init__(cls, mclass, members, options)
        cls.args = ArgsDict.struct(model=cls, args=(
          (name, a) for name, a in cls.members if ismodeledcfuncarg(a)))
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

Model.__name__ = 'cfunc.model.type'
