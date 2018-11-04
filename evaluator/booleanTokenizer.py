import ply.lex as lex
from ply.lex import TOKEN
import re
from decimal import Decimal, getcontext, ROUND_HALF_UP
from .exceptions import LexerInvalidToken
getcontext().prec = 8
getcontext().rounding = ROUND_HALF_UP

regex_or = r'\|\|?|[oO][rR]'
regex_and = r'&&?|[aA][nN][dD]'
regex_true = r'[sS][iI]|[tT][rR][uU][eE]'
regex_false = r'[nN][oO]|[fF][aA][lL][sS][eE]'
compiled_or = re.compile(regex_or)
compiled_and = re.compile(regex_and)
compiled_true = re.compile(regex_true)
compiled_false = re.compile(regex_false)

tokens = ('OR', 'AND', 'VAR', 'TRUE', 'FALSE', 'NOT', 'LPAREN', 'RPAREN', 'LT',
          'GT', 'EQ', 'LTE', 'GTE', 'INT', 'DECIMAL', 'MINUS', 'STRING')

t_OR = regex_or
t_NOT = r'~|¬'
t_AND = regex_and
t_LTE = r'<='
t_GTE = r'>='
t_LT = r'<'
t_GT = r'>'
t_EQ = r'=='
t_MINUS = r'-'
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_STRING(t):
    r'\"[^"]+\"|\'[^\']\''
    t.value = t.value[1:-1]
    return t


def t_DECIMAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = Decimal(t.value)
    return t


def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


@TOKEN(regex_true)
def t_TRUE(t):
    t.value = True
    return t


@TOKEN(regex_false)
def t_FALSE(t):
    t.value = False
    return t


def t_VAR(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    if compiled_or.fullmatch(t.value):
        t.type = 'OR'
    elif compiled_and.fullmatch(t.value):
        t.type = 'AND'
    elif compiled_true.fullmatch(t.value):
        t.type = 'TRUE'
        t.value = True
    elif compiled_false.fullmatch(t.value):
        t.type = 'FALSE'
        t.value = False
    return t


def t_error(t):
    raise LexerInvalidToken


t_ignore = ' \r\n\t'

boolean_lexer = lex.lex()
