import pytest
from cStringIO import StringIO
from puzzle25 import turing_steps

@pytest.fixture
def fp():
    fp =  'Begin in state A.\n'
    fp += 'Perform a diagnostic checksum after 6 steps.\n'
    fp += '\n'
    fp += 'In state A:\n'
    fp += '  If the current value is 0:\n'
    fp += '    - Write the value 1.\n'
    fp += '    - Move one slot to the right.\n'
    fp += '    - Continue with state B.\n'
    fp += '  If the current value is 1:\n'
    fp += '    - Write the value 0.\n'
    fp += '    - Move one slot to the left.\n'
    fp += '    - Continue with state B.\n'
    fp += '\n'
    fp += 'In state B:\n'
    fp += '  If the current value is 0:\n'
    fp += '    - Write the value 1.\n'
    fp += '    - Move one slot to the left.\n'
    fp += '    - Continue with state A.\n'
    fp += '  If the current value is 1:\n'
    fp += '    - Write the value 1.\n'
    fp += '    - Move one slot to the right.\n'
    fp += '    - Continue with state A.'
    return fp

def test_turing_steps(fp):
    assert turing_steps(StringIO(fp)) == 3
