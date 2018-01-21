import pytest
from cStringIO import StringIO
from puzzle20 import find_closest_particle, remove_colliding_particles

@pytest.fixture
def fp():
    fp =  'p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>\n'
    fp += 'p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>'
    return fp

@pytest.fixture
def fp2():
    fp =  'p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>\n'
    fp += 'p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>\n'
    fp += 'p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>\n'
    fp += 'p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>'
    return fp

def test_find_closest_particle(fp):
    assert find_closest_particle(StringIO(fp)) == 0

def test_remove_colliding_particles(fp2):
    assert remove_colliding_particles(StringIO(fp2)) == 1