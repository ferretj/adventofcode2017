import pytest
from puzzle03 import spiral_memory_steps, spiral_additive_higher

@pytest.mark.parametrize('n, steps', [
    (1, 0),
    (9, 2),
    (12, 3),
    (23, 2),
    (24, 3),
    (25, 4),
    (1024, 31),
])
def test_spiral_memory_steps(n, steps):
    assert spiral_memory_steps(n) == steps

@pytest.mark.parametrize('n, high', [
    (1, 2),
    (2, 4),
    (4, 5),
    (5, 10),
])
def test_spiral_additive_higher(n, high):
    assert spiral_additive_higher(n) == high
