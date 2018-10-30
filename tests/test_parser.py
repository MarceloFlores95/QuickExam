from evaluator import QuestionParser, ParserSyntaxError, ParserVariableNotFound
import pytest
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().rounding = ROUND_HALF_UP


def test_factor():
    assert QuestionParser().parse('3') == '3'


def test_sum():
    assert QuestionParser().parse('$(3+5)') == '8'


def test_sub():
    assert QuestionParser().parse('$(3-5)') == '-2'


def test_times():
    assert QuestionParser().parse('$(2*5)') == '10'


def test_divide():
    assert QuestionParser().parse('$(10/5)') == '2'


def test_exp():
    assert QuestionParser().parse('$(2^3)') == '8'


def test_paren():
    assert QuestionParser().parse('$((2*5)/(2*1))') == '5'


def test_ambiguity_1():
    assert QuestionParser().parse('$(3+4*5)') == '23'


def test_ambiguity_2():
    assert QuestionParser().parse('$(3+2^2)') == '7'


def test_ambiguity_3():
    assert QuestionParser().parse('$(2^2+2)') == '6'


def test_ambiguity_4():
    assert QuestionParser().parse('$(2+2^2)') == '6'


def test_ambiguity_5():
    assert QuestionParser().parse('$(4^5/3)') == '341.3'


def test_ambiguity_6():
    assert QuestionParser().parse('$((1/3)*4^5)') == '341.3'


def test_ambiguity_7():
    assert QuestionParser().parse('$(2^3^2)') == '512'


def test_variables():
    assert QuestionParser(a=1, b=5).parse('$(a+b)') == '6'


def test_decimal_1():
    assert QuestionParser().parse('$(2+2.5)') == '4.5'


def test_decimal_2():
    assert QuestionParser().parse('$(2.5+2)') == '4.5'


def test_decimal_3():
    assert QuestionParser().parse('$(3.5/2)') == '1.75'


def test_with_text():
    assert QuestionParser().parse('2+2=$(2+2)') == '2+2=4'


def test_with_text_2():
    assert QuestionParser(
        name='Juan').parse('Hola $(name) 2+2=$(2+2)') == 'Hola Juan 2+2=4'


def test_negative_number_1():
    assert QuestionParser().parse('$(-1)') == '-1'


def test_negative_number_2():
    assert QuestionParser().parse('$(2+(-3))') == '-1'


def test_negative_number_3():
    assert QuestionParser(a=2,b=3).parse('$(a+(-b))') == '-1'


def test_variable_not_found():
    with pytest.raises(ParserVariableNotFound):
        QuestionParser().parse('$(a+b)')


def test_syntax_error():
    with pytest.raises(ParserSyntaxError):
        QuestionParser().parse('$(3++2)')
