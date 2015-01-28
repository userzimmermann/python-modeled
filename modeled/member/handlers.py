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

"""modeled.member.handlers

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['Handlers']


class Handlers(list):
    def __init__(self, items=None):
        list.__init__(self)
        if items is not None:
            self += items

    def __call__(self, func):
        self.append(func)
        return func

    def __iadd__(self, items):
        if callable(items) and not isinstance(items, Handlers):
            #==> single handler
            self.append(items)
        else:
            #==> multiple handlers
            self.extend(items)

    def __isub__(self, items):
        if callable(items) and not isinstance(items, Handlers):
            #==> single handler
            self.remove(items)
        else:
            #==> multiple handlers
            for item in items:
                self.remove(item)
