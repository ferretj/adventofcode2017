import pytest
from cStringIO import StringIO
from puzzle02 import spreadsheet_checksum, spreadsheet_checksum_evendiv_v2

@pytest.fixture
def sheet():
    return StringIO('5 1 9 5\n7 5 3\n2 4 6 8')

@pytest.fixture
def sheet2():
    return StringIO('5 9 2 8\n9 4 7 3\n3 8 6 5')

def test_spreadsheet_checksum(sheet):
    assert spreadsheet_checksum(sheet) == 18

def test_spreadsheet_checksum_evendiv(sheet2):
    assert spreadsheet_checksum_evendiv_v2(sheet2) == 9