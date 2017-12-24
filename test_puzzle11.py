import pytest
from cStringIO import StringIO
from puzzle11 import hex_steps, max_hex_steps

@pytest.mark.parametrize('path, n_steps', [
    ('ne,ne,ne', 3),
    ('ne,ne,sw,sw', 0),
    ('ne,ne,s,s', 2),
    ('se,sw,se,sw,sw', 3),
])
def test_hex_steps(path, n_steps):
    assert hex_steps(StringIO(path)) == n_steps

@pytest.mark.parametrize('path, max_steps', [
    ('ne,ne,ne', 3),
    ('ne,ne,sw,sw', 2),
    ('ne,ne,s,s', 2),
    ('se,sw,se,sw,sw', 3),
])
def test_max_hex_steps(path, max_steps):
    assert max_hex_steps(StringIO(path)) == max_steps