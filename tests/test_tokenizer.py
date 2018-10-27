import pytest
from ExpressionEvaluator import lexer
from decimal import Decimal, getcontext
getcontext().prec = 4


def token_to_tuple(token):
    return (token.type, token.value)


def lexer_to_list():
    return [token_to_tuple(token) for token in lexer]


def test_one_operator():
    lexer.input('$(+)$')
    assert lexer_to_list() == [('START', '$('), ('PLUS', '+'), ('END', ')$')]


def test_simple_operation():
    lexer.input('$(3+5)$')
    assert lexer_to_list() == [('START', '$('), ('INT', 3), ('PLUS', '+'),
                               ('INT', 5), ('END', ')$')]


def test_character_ignore():
    lexer.input('$(3 + \t\n 5)$')
    assert lexer_to_list() == [('START', '$('), ('INT', 3), ('PLUS', '+'),
                               ('INT', 5), ('END', ')$')]


def test_decimal():
    lexer.input('$(2.15 + 3 - 4.2)$')
    assert lexer_to_list() == [('START', '$('), ('DECIMAL', Decimal('2.15')),
                               ('PLUS', '+'), ('INT', 3), ('MINUS', '-'),
                               ('DECIMAL', Decimal('4.2')), ('END', ')$')]


def test_text():
    lexer.input('Hola')
    assert lexer_to_list() == [('TEXT', 'Hola')]
