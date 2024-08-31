
import pytest
import util


def test_parse_contract() -> None:
    # doesn't end with 'ppp'
    with pytest.raises(AssertionError):
        util.parse_contract('1npp') == ''
    # bad character
    with pytest.raises(AssertionError):
        util.parse_contract('1npsp') == ''
    # bad suit
    with pytest.raises(AssertionError):
        util.parse_contract('1np2ap') == ''
    assert util.parse_contract('1nppp') == ['1n', 'p', 'p', 'p']
    assert util.parse_contract('1sp2dppp') == ['1s', 'p', '2d', 'p', 'p', 'p']
    assert util.parse_contract('1nxprppp') == \
           ['1n', 'x', 'p', 'r', 'p', 'p', 'p']

    assert util.parse_contract('p1nppp') == ['p', '1n', 'p', 'p', 'p']


def test_get_contract() -> None:
    assert util.get_contract('n', 'pppp') == ('n', 'pass')
    assert util.get_contract('n', '1sppp') == ('1s', 'n')
