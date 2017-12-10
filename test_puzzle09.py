import pytest
from cStringIO import StringIO
from puzzle09 import stream_group_score, garbage_count_before_group, stream_garbage_count

@pytest.mark.parametrize('stream, score', [
    ('{}', 1),
    ('{{{}}}', 6),
    ('{{},{}}', 5),
    ('{{{},{},{{}}}}', 16),
    ('{<a>,<a>,<a>,<a>}', 1),
    ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
    ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
    ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
])
def test_stream_group_score(stream, score):
    assert stream_group_score(StringIO(stream)) == score

@pytest.mark.parametrize('s, count', [
    ('<>', 0),
    ('<random characters>', 17),
    ('<<<<>', 3),
    ('<{!>}>', 2),
    ('<!!>', 0),
    ('<!!!>>', 0),
    ('<{o"i!a,<{i<a>', 10),
])
def test_garbage_count_before_group(s, count):
    assert garbage_count_before_group(list(s))[2] == count

@pytest.mark.parametrize('stream, count', [
    ('{}', 0),
    ('{{{}}}', 0),
    ('{{},{}}', 0),
    ('{{{},{},{{}}}}', 0),
    ('{<a>,<a>,<a>,<a>}', 4),
    ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 8),
    ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 0),
    ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 17),
])
def test_stream_garbage_count(stream, count):
    assert stream_garbage_count(StringIO(stream)) == count
