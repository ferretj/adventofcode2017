import pytest
from cStringIO import StringIO
from puzzle14 import used_squares, count_regions

@pytest.fixture
def fp():
    fp = 'flqrgnkx'
    return fp

def test_used_squares(fp):
    assert used_squares(StringIO(fp)) == 8108

def test_count_regions(fp):
    assert count_regions(StringIO(fp)) == 1242
