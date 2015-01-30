"""Test modeled.datetime (mdatetime)

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""

import pytest

from datetime import datetime

import modeled
from modeled import mdatetime


def test_class():
    """Test if modeled.datetime is derived from datetime.datetime

    - Tests implicitly if modeled.datetime is the class and not the submodule.
    """
    assert issubclass(modeled.datetime, datetime)


def test_alias():
    """Test if modeled.mdatetime alias is correctly assigned.
    """
    assert mdatetime is modeled.datetime


@pytest.fixture(scope='module', params=[
  (1, 2, 3),
  (1, 2, 3, 4, 5, 6),
  ])
def args(request):
    """Provide several init args,
       which work with both modeled.datetime and datetime.datetime
    """
    return request.param


def test_datetime(args):
    """Test modeled.datetime instantiation and usage.
    """
    basic_dt = datetime(*args)
    assert mdatetime(*args) == basic_dt
    assert mdatetime(str(basic_dt)) == basic_dt
