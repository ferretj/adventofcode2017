import pytest
from cStringIO import StringIO
from puzzle17 import first_value_cb

@pytest.fixture
def fp():
    fp = '3'
    return fp

def test_first_value_cb(fp):
    assert first_value_cb(StringIO(fp)) == 638
