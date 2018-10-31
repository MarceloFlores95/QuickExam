import ply.lex as lex
from decimal import Decimal, getcontext, ROUND_HALF_UP
from .exceptions import LexerInvalidToken

getcontext().rounding = ROUND_HALF_UP

states = (('exp', 'exclusive'), )

tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'RPAREN', 'LPAREN', 'VAR', 'INT',
          'DECIMAL', 'EXP', 'START', 'TEXT')


def t_START(t):
    r'\$\('
    t.lexer.paren_counter += 1
    t.lexer.begin('exp')
    return t


def t_error(t):
    raise LexerInvalidToken


def t_exp_LPAREN(t):
    r'\('
    t.lexer.paren_counter += 1
    return t


def t_exp_RPAREN(t):
    r'\)'
    t.lexer.paren_counter -= 1
    if t.lexer.paren_counter == 0:
        t.lexer.begin('INITIAL')
    return t


t_TEXT = r'[^$]+'
t_exp_PLUS = r'\+'
t_exp_MINUS = r'-'
t_exp_DIVIDE = r'/'
t_exp_TIMES = r'\*'
t_exp_EXP = r'\^'
t_exp_VAR = r'[a-zA-Z][a-zA-Z_0-9]*'


def t_exp_DECIMAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = Decimal(t.value)
    return t


def t_exp_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


t_exp_ignore = ' \t\n\r'

question_lexer = lex.lex()
question_lexer.paren_counter = 0
