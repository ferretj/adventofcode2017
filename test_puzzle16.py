import pytest
import string
from cStringIO import StringIO
from puzzle16 import dancing_permutation

@pytest.fixture
def l():
    l = list(string.ascii_lowercase)[:5]
    return l

@pytest.fixture
def fp():
    fp =  's1,x3/4,pe/b'
    return fp

def test_dancing_permutation(fp, l):
    ll = dancing_permutation(l, StringIO(fp))
    assert ''.join(ll) == 'baedc'
