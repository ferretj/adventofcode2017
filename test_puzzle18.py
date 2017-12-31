import pytest
from cStringIO import StringIO
from puzzle18 import recover_freq, duet

@pytest.fixture
def fp():
    fp =  'set a 1\n'
    fp += 'add a 2\n'
    fp += 'mul a a\n'
    fp += 'mod a 5\n'
    fp += 'snd a\n'
    fp += 'set a 0\n'
    fp += 'rcv a\n'
    fp += 'jgz a -1\n'
    fp += 'set a 1\n'
    fp += 'jgz a -2'
    return fp

@pytest.fixture
def fp2():
    fp =  'snd 1\n'
    fp += 'snd 2\n'
    fp += 'snd p\n'
    fp += 'rcv a\n'
    fp += 'rcv b\n'
    fp += 'rcv c\n'
    fp += 'rcv d\n'
    return fp

def test_recover_freq(fp):
    assert recover_freq(StringIO(fp)) == 4

def test_duet(fp2):
    assert duet(StringIO(fp2)) == 3
