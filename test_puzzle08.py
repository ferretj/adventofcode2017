import pytest
from cStringIO import StringIO
from puzzle08 import largest_register_value, largest_intermediate_register_value

@pytest.fixture
def instructions():
    ls = 'b inc 5 if a > 1'
    ls += '\na inc 1 if b < 5'
    ls += '\nc dec -10 if a >= 1'
    ls += '\nc inc -20 if c == 10'
    return ls

def test_largest_register_value(instructions):
    assert largest_register_value(StringIO(instructions)) == 1

def test_largest_intermediate_register_value(instructions):
    assert largest_intermediate_register_value(StringIO(instructions)) == 10
