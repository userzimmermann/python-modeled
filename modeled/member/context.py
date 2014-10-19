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

"""modeled.member.context

Provides a context manager for modeled.object
to work with temporarily changed member values in a with block.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""


class context(dict):
    def __init__(self, members, mapping=None, **membervalues):
        if mapping:
            dict.__init__(self, mapping, **membervalues)
        else:
            dict.__init__(self, **membervalues)
        self.members = members

    def __enter__(self):
        self.mbackup = {membername: self.members[membername].value
                        for membername in self}
        for membername, value in self.items():
            self.members[membername].value = value

    def __exit__(self, *exc):
        for membername, value in self.mbackup.items():
            self.members[membername].value = value
