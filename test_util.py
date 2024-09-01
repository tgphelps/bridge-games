
import pytest
import util


def test_parse_contract() -> None:
    # doesn't end with 'ppp'
    with pytest.raises(AssertionError):
        util._parse_contract('1npp') == ''
    # bad character
    with pytest.raises(AssertionError):
        util._parse_contract('1npsp') == ''
    # bad suit
    with pytest.raises(AssertionError):
        util._parse_contract('1np2ap') == ''
    assert util._parse_contract('1nppp') == ['1n', 'p', 'p', 'p']
    assert util._parse_contract('1sp2dppp') == ['1s', 'p', '2d', 'p', 'p', 'p']
    assert util._parse_contract('1nxprppp') == \
           ['1n', 'x', 'p', 'r', 'p', 'p', 'p']

    assert util._parse_contract('p1nppp') == ['p', '1n', 'p', 'p', 'p']


def test_passed_out() -> None:
    test_cases = [
        ('n', 'pppp', 'N', 'PASS')
    ]
    run_test_cases(test_cases)


def test_simple_auction() -> None:
    test_cases = [
        ('n', '1sppp', '1S', 'N'),
        ('s', '1sppp', '1S', 'S'),
        ('e', '1sp3sppp', '3S', 'E'),
        ('w', '1sx2s3hpp3sppp', '3S', 'W'),
    ]
    run_test_cases(test_cases)


def test_doubled_auction() -> None:
    test_cases = [
        ('n', '1sxppp', '1SX', 'N'),
        ('n', '1sxpprppp', '1SXX', 'N'),
        ('s', 'pp1hp2hppxppp', '2HX', 'N'),
        ('e', '1np2cp2hp3nxpprppp', '3NXX', 'E'),
        ('w', '1s2sp3sxrppp', '3SXX', 'N')
    ]
    run_test_cases(test_cases)


def run_test_cases(test_cases: list[tuple[str, str, str, str]]) -> None:
    for item in test_cases:
        assert util.get_contract(item[0], item[1]) == (item[2], item[3])
