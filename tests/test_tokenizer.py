import pytest
from ExpressionEvaluator import lexer
from decimal import Decimal, getcontext
getcontext().prec = 4


def token_to_tuple(token):
    return (token.type, token.value)


def lexer_to_list(lexer):
    return [token_to_tuple(token) for token in lexer]


def test_one_operator_1():
    lex = lexer.clone()
    lex.input('$(+)')
    assert lexer_to_list(lex) == [('START', '$('), ('PLUS', '+'),
                                  ('RPAREN', ')')]


def test_one_operator_2():
    lex = lexer.clone()
    lex.input('$(-)')
    assert lexer_to_list(lex) == [('START', '$('), ('MINUS', '-'),
                                  ('RPAREN', ')')]


def test_simple_operation():
    lex = lexer.clone()
    lex.input('$(3+5)')
    assert lexer_to_list(lex) == [('START', '$('), ('INT', 3), ('PLUS', '+'),
                                  ('INT', 5), ('RPAREN', ')')]


def test_character_ignore():
    lex = lexer.clone()
    lex.input('$(3 + \t\n 5)')
    assert lexer_to_list(lex) == [('START', '$('), ('INT', 3), ('PLUS', '+'),
                                  ('INT', 5), ('RPAREN', ')')]


def test_decimal():
    lex = lexer.clone()
    lex.input('$(2.15 + 3 - 4.2)')
    assert lexer_to_list(lex) == [('START', '$('), ('DECIMAL',
                                                    Decimal('2.15')),
                                  ('PLUS', '+'), ('INT', 3), ('MINUS', '-'),
                                  ('DECIMAL', Decimal('4.2')), ('RPAREN', ')')]


def test_text():
    lex = lexer.clone()
    lex.input('Hola')
    assert lexer_to_list(lex) == [('TEXT', 'Hola')]
