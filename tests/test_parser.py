from ExpressionEvaluator import Parser


def test_factor():
    assert Parser().parse('3') == 3


def test_sum():
    assert Parser().parse('3+5') == 8


def test_ambiguity_1():
    assert Parser().parse('3+4*5') == 23


def test_variables():
    assert Parser(a=1, b=5).parse('a+b') == 6
