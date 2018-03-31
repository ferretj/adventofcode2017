import pytest
from cStringIO import StringIO
from puzzle24 import strongest_bridge, longest_bridge

@pytest.fixture
def fp():
    fp =  '0/2\n'
    fp +=  '2/2\n'
    fp +=  '2/3\n'
    fp +=  '3/4\n'
    fp +=  '3/5\n'
    fp +=  '0/1\n'
    fp +=  '10/1\n'
    fp +=  '9/10'
    return fp

def test_strongest_bridge(fp):
    assert strongest_bridge(StringIO(fp)) == 31

def test_longest_bridge(fp):
    assert longest_bridge(StringIO(fp)) == 19
