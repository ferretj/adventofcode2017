import pytest
from cStringIO import StringIO
from puzzle13 import firewall_severity, find_delay

@pytest.fixture
def fp():
    fp = '0: 3\n'
    fp += '1: 2\n'
    fp += '4: 4\n'
    fp += '6: 4'
    return fp

def test_firewall_severity(fp):
    assert firewall_severity(StringIO(fp)) == 24

def test_find_delay(fp):
    assert find_delay(StringIO(fp)) == 10
