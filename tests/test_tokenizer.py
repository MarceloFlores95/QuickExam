import pytest
from ExpressionEvaluator import lexer


def token_to_tuple(token):
    return (token.type, token.value)


def lexer_to_list(lex):
    return [token_to_tuple(token) for token in lexer]


def test_one_operator():
    lexer.input('+')
    assert lexer_to_list(lexer) == [('PLUS', '+')]

