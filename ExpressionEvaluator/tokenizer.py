import ply.lex as lex
from decimal import Decimal, getcontext

getcontext().prec = 4

tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'RPAREN', 'LPAREN', 'VAR', 'INT',
          'DECIMAL', 'EXP')

t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_TIMES = r'\*'
t_EXP = r'\^'
t_RPAREN = r'\('
t_LPAREN = r'\)'
t_VAR = r'[a-zA-Z][a-zA-Z_0-9]*'


def t_DECIMAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = Decimal(t.value)
    return t


def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


t_ignore = ' \t\n\r'

lexer = lex.lex()
