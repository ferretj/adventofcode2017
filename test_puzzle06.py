from cStringIO import StringIO
from puzzle06 import memory_reallocation_cycles, memory_reallocation_cycles_min

def test_memory_reallocation_cycles():
    s = StringIO('0\t2\t7\t0')
    assert memory_reallocation_cycles(s) == 5

def test_memory_reallocation_cycles_min():
    s = StringIO('0\t2\t7\t0')
    assert memory_reallocation_cycles_min(s) == 4
