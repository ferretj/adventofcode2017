import pytest
from cStringIO import StringIO
from puzzle07 import find_bottom_program, balance_weight

@pytest.fixture
def program_list():
    pl = 'pbga (66)\nxhth (57)\nebii (61)\nhavc (66)\nktlj (57)\n'
    pl += 'fwft (72) -> ktlj, cntj, xhth\nqoyq (66)\npadx (45) -> '
    pl += 'pbga, havc, qoyq\ntknk (41) -> ugml, padx, fwft\n'
    pl += 'jptl (61)\nugml (68) -> gyxo, ebii, jptl\ngyxo (61)\ncntj (57)'
    return pl

def test_find_bottom_program(program_list):
    assert find_bottom_program(StringIO(program_list)) == 'tknk'

def test_balance_weight(program_list):
    assert balance_weight(StringIO(program_list)) == 60
