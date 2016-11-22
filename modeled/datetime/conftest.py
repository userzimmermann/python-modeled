import pytest


@pytest.fixture(scope='module', params=[
    (1, 2, 3),
    (1, 2, 3, 4, 5, 6),
])
def args(request):
    return request.param


@pytest.fixture(scope='module', params=[
    "%Y/%m/%d %H-%M-%S",
    "%d.%m.%Y %H:%M:%S",
])
def format(request):
    return request.param
