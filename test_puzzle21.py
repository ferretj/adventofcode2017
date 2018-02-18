import pytest
from cStringIO import StringIO
from puzzle21 import fractal_augment

@pytest.fixture
def fp():
    fp =  '../.# => ##./#../...\n'
    fp += '.#./..#/### => #..#/..../..../#..#'
    return fp

def test_pixels_on(fp):
    grid = fractal_augment(StringIO(fp), 2)
    assert grid.n_pixels == 12
