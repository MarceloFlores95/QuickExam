import ply.yacc as yacc
from .booleanTokenizer import tokens, boolean_lexer
from .exceptions import ParserSyntaxError, ParserVariableNotFound


class BooleanParser:
    def __init__(self, **kwargs):
        self.table = kwargs
        self.tokens = tokens
        self.parser = yacc.yacc(module=self, tabmodule='booleanParseTab')

    def p_or_expression(self, p):
        'expression: expression OR term'
        p[0] = p[1] or p[3]

    def p_expression_term(self, p):
        'expression: term'
        p[0] = p[1]

    def p_and_term(self, p):
        'term: term AND boolean'
        p[0] = p[1] and p[3]


    def p_term_boolean(self, p):
        'boolean: term'
        p[0] = p[1]

    def p_boolean_true(self, p):
        'boolean: TRUE'
        p[0] = p[1]

    def p_boolean_false(self, p):
        'boolean: FALSE'
        p[0] = p[1]

    def p_not_boolean(self, p):
        'boolean: NOT boolean'
        p[0] = not p[2]

    def p_boolean_expression(self, p):
        'boolean: LPAREN expression RPAREN'
        p[0] = p[2]
