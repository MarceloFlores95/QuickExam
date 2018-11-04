from evaluator import QuestionParser, ParserSyntaxError, ParserVariableNotFound
import pytest
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().rounding = ROUND_HALF_UP

parser = QuestionParser()


def test_factor():
    assert parser.parse('3') == '3'


def test_sum():
    assert parser.parse('$(3+5)') == '8'


def test_sub():
    assert parser.parse('$(3-5)') == '-2'


def test_times():
    assert parser.parse('$(2*5)') == '10'


def test_divide():
    assert parser.parse('$(10/5)') == '2'


def test_exp():
    assert parser.parse('$(2^3)') == '8'


def test_paren():
    assert parser.parse('$((2*5)/(2*1))') == '5'


def test_ambiguity_1():
    assert parser.parse('$(3+4*5)') == '23'


def test_ambiguity_2():
    assert parser.parse('$(3+2^2)') == '7'


def test_ambiguity_3():
    assert parser.parse('$(2^2+2)') == '6'


def test_ambiguity_4():
    assert parser.parse('$(2+2^2)') == '6'


def test_ambiguity_5():
    assert parser.parse('$(4^5/3)') == '341.33333'


def test_ambiguity_6():
    assert parser.parse('$((1/3)*4^5)') == '341.33333'


def test_ambiguity_7():
    assert parser.parse('$(2^3^2)') == '512'


def test_variables():
    assert QuestionParser(a=1, b=5).parse('$(a+b)') == '6'


def test_decimal_1():
    assert parser.parse('$(2+2.5)') == '4.5'


def test_decimal_2():
    assert parser.parse('$(2.5+2)') == '4.5'


def test_decimal_3():
    assert parser.parse('$(3.5/2)') == '1.75'


def test_with_text():
    assert parser.parse('2+2=$(2+2)') == '2+2=4'


def test_with_text_2():
    assert QuestionParser(
        name='Juan').parse('Hola $(name) 2+2=$(2+2)') == 'Hola Juan 2+2=4'


def test_negative_number_1():
    assert parser.parse('$(-1)') == '-1'


def test_negative_number_2():
    assert parser.parse('$(2+(-3))') == '-1'


def test_negative_number_3():
    assert QuestionParser(a=2, b=3).parse('$(a+(-b))') == '-1'


def test_negative_number_4():
    assert parser.parse('$(-(2+3))') == '-5'


def test_negative_number_5():
    assert parser.parse('$(5+(-(2+3)))') == '0'


def test_redundant_paren_1():
    assert parser.parse('$((2+3))') == '5'


def test_redundant_paren_1():
    assert parser.parse('$((2)+(3))') == '5'


def test_text_1():
    assert parser.parse('$$(1)') == '$1'

def test_redundant_paren_3():
    assert parser.parse('$((10 / 5) * 2)') == '4'


def test_variable_not_found():
    with pytest.raises(ParserVariableNotFound):
        parser.parse('$(a+b)')


def test_syntax_error():
    with pytest.raises(ParserSyntaxError):
        parser.parse('$(3++2)')
