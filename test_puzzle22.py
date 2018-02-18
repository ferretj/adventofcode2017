import pytest
from cStringIO import StringIO
from puzzle22 import activity_bursts, activity_bursts_updated

@pytest.fixture
def fp():
    fp =  '..#\n'
    fp += '#..\n'
    fp += '...'
    return fp

def test_activity_bursts(fp):
    assert activity_bursts(StringIO(fp), 10000) == 5587

def test_activity_bursts_updated(fp):
    assert activity_bursts_updated(StringIO(fp), 100) == 26
    assert activity_bursts_updated(StringIO(fp), 10000000) == 2511944
