"""Test :mod:`modeled.base`

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
import warnings
from inspect import getmembers

from moretools import dictvalues

from modeled.base import metabase, base
import modeled

import pytest


def test_metabase():
    """Test :class:`modeled.base.metabase`.
    """
    # should not be available in modeled top-level
    assert metabase not in dictvalues(dict(getmembers(modeled)))

    # check convenience classmethod for getting mro of metaclass
    assert metabase.metamro() == metabase.mro(metabase)


def test_base():
    """Test :class:`modeled.base.base`.
    """
    # should not be available in modeled top-level
    assert base not in dictvalues(dict(getmembers(modeled)))

    # check metaclass and .meta property
    assert base.meta is type(base) is metabase
    # and deprecation of .type property
    with pytest.warns(DeprecationWarning), warnings.catch_warnings():
        warnings.simplefilter('always')
        assert base.type is metabase

    # check convenience classmethod for getting mro of metaclass
    assert base.metamro() == metabase.mro(metabase)
