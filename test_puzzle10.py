import pytest
from cStringIO import StringIO
from puzzle10 import knot_hash_first_two_elems, knot_hash

def test_knot_hash_first_two_elems():
    kh = knot_hash_first_two_elems(StringIO('3,4,1,5'), 5)
    assert kh == 12

@pytest.mark.parametrize('seq, h', [
    ('',         'a2582a3a0e66e6e86e3812dcb672a272'),
    ('AoC 2017', '33efeb34ea91902bb2f59c9920caa6cd'),
    ('1,2,3',    '3efbe78a8d82f29979031a4aa0b16a9d'),
    ('1,2,4',    '63960835bcdc130f0b66d7ff4f6a5a8e'),
])
def test_knot_hash(seq, h):
    assert knot_hash(StringIO(seq), 256) == h