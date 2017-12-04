import pytest
from cStringIO import StringIO
from puzzle04 import check_passphrases, check_passphrases_anagrams

@pytest.mark.parametrize('passw, is_valid', [
    ('aa bb cc dd ee', True),
    ('aa bb cc dd aa', False),
    ('aa bb cc dd aaa', True)
])
def test_check_passphrases(passw, is_valid):
    assert bool(check_passphrases(StringIO(passw))) == is_valid

@pytest.mark.parametrize('passw, is_valid', [
    ('abcde fghij', True),
    ('abcde xyz ecdab', False),
    ('a ab abc abd abf abj', True),
    ('iiii oiii ooii oooi oooo', True),
    ('oiii ioii iioi iiio', False)
])
def test_check_passphrases_anagrams(passw, is_valid):
    assert bool(check_passphrases_anagrams(StringIO(passw))) == is_valid
