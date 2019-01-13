from Practicum1 import IncorrectDataError
from Practicum1 import findMaxXLen
import pytest


def test_samples():
    assert findMaxXLen("ab+c.aba.*.bac.+.+*", 'a') == 2
    assert findMaxXLen("acb..bab.c.*.ab.ba.+.+*a.", 'a') == 2


def test_just_string():
    string = "bcc..cb.*ccb...."
    symbol = "c"
    assert findMaxXLen(string, symbol) == 4


def test_empty_test():
    assert findMaxXLen("", 'a') == 0


def test_incorrect_x():
    with pytest.raises(IncorrectDataError):
        string = "ab.*1+ab.*."
        symbol = "d"
        findMaxXLen(string, symbol)


class TestIncorrectStrings:
    def test_overflow(self):
        with pytest.raises(IncorrectDataError):
            findMaxXLen("a1+bc.", 'a')
        with pytest.raises(IncorrectDataError):
            findMaxXLen("ab.ca+.*abc.", 'a')

    def test_underflow(self):
        # в стеке недостаточно элементов перед выполнением операции "*"
        with pytest.raises(IncorrectDataError):
            findMaxXLen("*ab.", 'a')

        # в стеке недостаточно элементов перед выполнением операции "+"
        with pytest.raises(IncorrectDataError):
            findMaxXLen("ab.+", 'a')
        with pytest.raises(IncorrectDataError):
            findMaxXLen("+ab.", 'a')

        # в стеке недостаточно элементов перед выполнением операции "."
        with pytest.raises(IncorrectDataError):
            findMaxXLen("ab+.", 'a')
        with pytest.raises(IncorrectDataError):
            findMaxXLen("+ab", 'a')

    def test_incorrect_symbol(self):
        with pytest.raises(IncorrectDataError):
            findMaxXLen("ab-", 'a')


def test_symbol_not_in_string():
    assert findMaxXLen("a1.b.*", 'c') == 0
    assert findMaxXLen("ac.*", 'b') == 0
    assert findMaxXLen("b1+c*+", 'a') == 0


def test_infinity():
    assert findMaxXLen("cb.ab+*+1.", 'a') == "INF"
