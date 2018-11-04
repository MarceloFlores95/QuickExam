from evaluator import BooleanParser, ParserSyntaxError
import pytest

parser = BooleanParser()


def test_comparison_1():
    assert parser.parse('1==1') == True


def test_comparison_2():
    assert parser.parse('3<3') == False


def test_comparison_3():
    assert parser.parse('3<=3') == True


def test_comparison_4():
    assert parser.parse('4<=3') == False


def test_comparison_5():
    assert parser.parse('2.15==2.15') == True


def test_comparison_5():
    assert parser.parse('2.15==2.16') == False


def test_and_1():
    assert parser.parse('true and true') == True


def test_and_2():
    assert parser.parse('true and false') == False


def test_and_3():
    assert parser.parse('3 > 2 and 4 < 5') == True


def test_or_1():
    assert parser.parse('true or false') == True


def test_or_2():
    assert parser.parse('2 > 3 or 3 > 2') == True


def test_or_3():
    assert parser.parse('2 < 1 or 1 == 2') == False


def test_or_4():
    assert BooleanParser(a=3, b=5).parse('a==3 or b <= 10') == True


def test_negation_1():
    assert parser.parse('~true') == False


def test_negation_2():
    assert parser.parse('¬(false)') == True


def test_spaces():
    with pytest.raises(ParserSyntaxError):
        parser.parse('trueandfalse')


def test_string_comp_1():
    assert parser.parse('"Hola"=="Hola"') == True


def test_string_comp_2():
    assert parser.parse('"Hola"=="Adios"') == False


def test_string_comp_3():
    assert BooleanParser(name='Juan').parse('name=="Juan"') == True
