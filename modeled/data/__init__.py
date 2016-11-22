# MODELED | Universal data modeling for Python
#
# Copyright (C) 2014-2016 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# MODELED is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MODELED is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with MODELED.  If not, see <http://www.gnu.org/licenses/>.

"""modeled.data

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

import builtins

import modeled
from modeled.member.handlers import Handlers


class data(modeled.member):
    """
    Base class for defining MODELED typed data members in
    :class:`modeled.object` definitions.
    """
    strict = False

    def __init__(self, *default, **options):
        """
        Creates a typed :class:`modeled.object` data member
        with an optional `default` value, which can also be used as implicit
        data type provider:

        >>> class Code(modeled.object):
        ...     language = modeled.data[str]('python')

        >>> Code.language
        modeled.data[str]('python')

        By default, the member name is taken from the attribute name:

        >>> Code.language.name
        'language'

        The members can also be accessed from the MODELED class' ``.model``
        manager:

        >>> Code.model.members.language
        modeled.data[str]('python')

        >>> builtins.list(Code.model.members())
        [('language', modeled.data[str]('python'))]
        """
        modeled.member.__init__(self, **options)
        # strict data type checking requested?
        if 'strict' in options:
            self.strict = bool(options.pop('strict'))
        # set data type/default and options
        try:
            _type = self.type
        except AttributeError:
            assert(len(default) == 1)
            default = self.default = default[0]
            self.__class__ = type(self)[type(default)]
        else:
            if default:
                self.default = _type(*default)
        try:
            options = options['options']
        except KeyError:
            pass
        try:
            newfunc = options.pop('new')
        except KeyError:
            self.new = self.type
        else:
            new = self.new
            self.new = lambda value, func=newfunc: new(value, func)
            self.new.func = newfunc
        try:
            changed = options.pop('changed')
        except KeyError:
            self.changed = Handlers()
        else:
            self.changed = Handlers(changed)
        self.format = options.pop('format', None)
        try:  # were choices already defined on class level?
            self.choices
        except AttributeError:
            choices = options.pop('choices', None)
            self.choices = choices and builtins.list(choices)

    def __get__(self, obj, owner=None):
        """
        Get the current data member value from :class:`modeled.instancemember`
        object in ``obj.__dict__``.
        """
        if obj is None:  # ==> Accessed from modeled.object class level
            return self
        # get the instancemember for the given object
        target = obj.__dict__[self.name]
        try:  # it acts as value storage
            return target._value
        except AttributeError:
            try:
                return self.default
            except AttributeError:
                raise type(self).error("%s has no default value."
                                       % repr(self))

    def __set__(self, obj, value):
        """
        Stores a new data member `value` in ``obj.__dict__``.

        * If not ``self.strict``, the `value` is converted to member data type
          (by instantiating the type with `value`).
        * Afterwards the ``self.changed`` reactions are called.
        """
        if value is not None and not isinstance(value, self.type):
            if self.strict:
                raise modeled.strict.TypeError(
                    "%s got a %s value: %s"
                    % (repr(self), type(value), repr(value)))
            value = self.new(value)
        if self.choices and value not in self.choices:
            raise type(self).error("not a valid choice for '%s': %s"
                                   % (self.name, repr(value)))
        # get the instancemember for the given object
        target = obj.__dict__[self.name]
        target._value = value  # which also acts as value storage
        # finally call reactions. first from modeled class level
        for func in self.changed:
            func(obj, value)
        # then from instancemember level:
        for func in target.changed:
            func(value)

    def __repr__(self):
        result = "modeled." + type(self).__name__
        try:
            default = self.default
        except AttributeError:
            return result + "()"
        return result + "(%s)" % repr(default)

    def istuple(self):
        """
        Check if MODELED data member has tuple-based data type:

        >>> modeled.data[builtins.tuple]().istuple()
        True
        >>> modeled.data.tuple[str, int, float]().istuple()
        True
        """
        return issubclass(self.type, builtins.tuple)

    def islist(self):
        """
        Check if MODELED data member has list-based data type:

        >>> modeled.data[builtins.list]().islist()
        True
        >>> modeled.data.list[str]().islist()
        True
        """
        return issubclass(self.type, builtins.list)

    def isdict(self):
        """
        Check if MODELED data member has dict-based data type:

        >>> modeled.data[builtins.dict]().isdict()
        True
        >>> modeled.data.dict[str, int]().isdict()
        True
        """
        return issubclass(self.type, builtins.dict)


from .tuple import tuple
data.tuple = tuple

from .list import list
data.list = list

from .dict import dict
data.dict = dict
