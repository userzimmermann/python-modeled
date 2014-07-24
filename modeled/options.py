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

"""modeled.options

Provides the moretools.simpledict based Options class
for <modeled.object>.model.options.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['OptionError', 'Options']

from inspect import isclass, getmembers

from moretools import simpledict, SimpleDictType, SimpleDictStructType

# Imported at bottom:
# - from modeled.model import modelbase


class OptionError(Exception):
    __module__ = 'modeled'

OptionError.__name__ = 'modeled.OptionError'


class OptionsType(SimpleDictType):
    """`basetype` for `simpledict()` to create Options class.
    """
    def __init__(self, mapping=()):
        """Initialize an Options instance
           from an options `mapping` resulting from user-defined `class model`
           of a :class:`modeled.object` based class definition.
        """
        options = {} # Intermediate dict to separate option groups
        for opt, value in dict(mapping).items():
            try:
                optgroup, opt = opt.split('__', 1)
            except ValueError:
                if isclass(value):
                    value = getmembers(value)
                try:
                    value = dict(value)
                except (TypeError, ValueError):
                    options[opt] = value
                    continue

                optgroup = opt
                options[optgroup] = Options(value)
                continue

            options.setdefault(optgroup, Options())[opt] = value

        SimpleDictType.__init__(
          self, {opt: value for opt, value in dict(options).items()
                 if opt and not opt.startswith('_')})


class OptionsStructType(SimpleDictStructType):
    """`basestructtype` for `simpledict()` to create Options.struct class.
    """
    def __init__(self, model, options=()):
        """Initialize an Options.struct instance
           with the associated <modeled.object>.`model` instance
           and an `options` mapping resulting from user-defined `class model`
           of a :class:`modeled.object` based class definition.
        """
        def bases():
            for cls in model.__bases__:
                if cls is not modelbase:
                    yield cls.options
        # Delegates options to OptionsType.__init__()
        SimpleDictStructType.__init__( # First arg is struct __name__
          self, '%s.options' % repr(model), bases(), options)


Options = simpledict(
  'Options', basetype=OptionsType, basestructtype=OptionsStructType)


from modeled.model import modelbase
