import pytest
from cStringIO import StringIO
from puzzle05 import twisty_trampoline_steps, twisty_trampoline_steps_3m

@pytest.fixture
def seq():
    return '0\n3\n0\n1\n-3'

def test_twisty_trampoline_steps(seq):
    assert twisty_trampoline_steps(StringIO(seq)) == 5

def test_twisty_trampoline_steps_3m(seq):
    assert twisty_trampoline_steps_3m(StringIO(seq)) == 10
