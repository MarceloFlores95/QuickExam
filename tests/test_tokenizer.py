import pytest
from evaluator import question_lexer
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().rounding = ROUND_HALF_UP


def token_to_tuple(token):
    return (token.type, token.value)


def lexer_to_list(lexer):
    return [token_to_tuple(token) for token in lexer]


def test_one_operator_1():
    lex = question_lexer.clone()
    lex.input('$(+)')
    assert lexer_to_list(lex) == [('START', '$('), ('PLUS', '+'),
                                  ('RPAREN', ')')]


def test_one_operator_2():
    lex = question_lexer.clone()
    lex.input('$(-)')
    assert lexer_to_list(lex) == [('START', '$('), ('MINUS', '-'),
                                  ('RPAREN', ')')]


def test_simple_operation():
    lex = question_lexer.clone()
    lex.input('$(3+5)')
    assert lexer_to_list(lex) == [('START', '$('), ('INT', 3), ('PLUS', '+'),
                                  ('INT', 5), ('RPAREN', ')')]


def test_character_ignore():
    lex = question_lexer.clone()
    lex.input('$(3 + \t\n 5)')
    assert lexer_to_list(lex) == [('START', '$('), ('INT', 3), ('PLUS', '+'),
                                  ('INT', 5), ('RPAREN', ')')]


def test_decimal():
    lex = question_lexer.clone()
    lex.input('$(2.15 + 3 - 4.2)')
    assert lexer_to_list(lex) == [('START', '$('), ('DECIMAL',
                                                    Decimal('2.15')),
                                  ('PLUS', '+'), ('INT', 3), ('MINUS', '-'),
                                  ('DECIMAL', Decimal('4.2')), ('RPAREN', ')')]


def test_text_1():
    lex = question_lexer.clone()
    lex.input('Hola')
    assert lexer_to_list(lex) == [('CHAR', 'H'), ('CHAR', 'o'), ('CHAR', 'l'),
                                  ('CHAR', 'a')]


def test_text_2():
    lex = question_lexer.clone()
    lex.input('$$()')
    assert lexer_to_list(lex) == [('CHAR', '$'), ('START', '$('),
                                  ('RPAREN', ')')]
