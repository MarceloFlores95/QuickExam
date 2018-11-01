import ply.lex as lex
import re
from .exceptions import LexerInvalidToken

tokens = ('OR', 'AND', 'VAR', 'TRUE', 'FALSE', 'NOT')

t_OR = r'(?i)\|\|?|or'
t_NOT = r'~|¬'
t_AND = r'(?i)&&?|and'
t_VAR = r'[a-zA-Z][a-zA-Z0-9_]*'


def t_TRUE(t):
    r'(?i)1|si|true'
    t.value = True
    return t


def t_FALSE(t):
    r'(?i)0|no|false'
    t.value = False
    return t


def t_error(t):
    raise LexerInvalidToken


t_ignore = ' \r\n\t'

boolean_lexer = lex()
