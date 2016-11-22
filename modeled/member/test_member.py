import modeled

import pytest


class TestMember(object):

    def test_class__getitem__(self):
        assert modeled.member[int].mtype is int
        with pytest.raises(TypeError):
            assert modeled.member[2]
