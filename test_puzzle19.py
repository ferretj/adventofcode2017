import pytest
from cStringIO import StringIO
from puzzle19 import route

@pytest.fixture
def fp():
    fp =  '     |          \n'
    fp += '     |  +--+    \n'
    fp += '     A  |  C    \n'
    fp += ' F---|----E|--+ \n'
    fp += '     |  |  |  D \n'
    fp += '     +B-+  +--+   '
    return fp

def test_route(fp):
    assert route(StringIO(fp))[0] == 'ABCDEF'

def test_route_steps(fp):
    assert route(StringIO(fp))[1] == 38
