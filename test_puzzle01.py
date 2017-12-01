import pytest
from puzzle01 import solve_captcha_next, solve_captcha_halfway

@pytest.mark.parametrize('capt, res', [
    ('1122', 3),
    ('1111', 4),
    ('1234', 0),
    ('91212129', 9),
])
def test_solve_captcha_next(capt, res):
    assert solve_captcha_next(capt) == res


@pytest.mark.parametrize('capt, res', [
    ('1212', 6),
    ('1221', 0),
    ('123425', 4),
    ('123123', 12),
    ('12131415', 4),
])
def test_solve_captcha_halfway(capt, res):
    assert solve_captcha_halfway(capt) == res