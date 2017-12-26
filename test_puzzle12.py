import pytest
from cStringIO import StringIO
from puzzle12 import zero_connected_programs, program_groups

@pytest.fixture
def fp():
    fp = "0 <-> 2"
    fp += "\n1 <-> 1"
    fp += "\n2 <-> 0, 3, 4"
    fp += "\n3 <-> 2, 4"
    fp += "\n4 <-> 2, 3, 6"
    fp += "\n5 <-> 6"
    fp += "\n6 <-> 4, 5"
    return fp

def test_zero_connected_programs(fp):
    assert zero_connected_programs(StringIO(fp)) == 6

def test_program_groups(fp):
    assert program_groups(StringIO(fp)) == 2
