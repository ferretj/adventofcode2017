import pytest
from cStringIO import StringIO
from puzzle15 import judge_count, judge_count_v2

@pytest.fixture
def fp():
    fp =  'Generator A starts with 65\n'
    fp += 'Generator B starts with 8921\n'
    return fp

def test_judge_count(fp):
    assert judge_count(StringIO(fp), 40000000) == 588

def test_judge_count_v2(fp):
    assert judge_count_v2(StringIO(fp), 5000000) == 309
