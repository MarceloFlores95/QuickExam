import ply.yacc as yacc
from .booleanTokenizer import tokens, boolean_lexer
from .exceptions import ParserSyntaxError, ParserVariableNotFound


class BooleanParser:
    def __init__(self, **kwargs):
        self.table = kwargs
        self.tokens = tokens
        self.parser = yacc.yacc(module=self, tabmodule='booleanParseTab')

    def parse(self, s: str) -> bool:
        return self.parser(s, lexer=boolean_lexer.clone())

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
        'term: boolean'
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

    def p_boolean_lt(self, p):
        'boolean: factor LT factor'
        p[0] = p[1] < p[3]

    def p_boolean_gt(self, p):
        'boolean: factor GT factor'
        p[0] = p[1] > p[3]

    def p_boolean_eq(self, p):
        'boolean: factor EQ factor'
        p[0] = p[1] == p[3]

    def p_boolean_lte(self, p):
        'boolean: factor LTE factor'
        p[0] = p[1] <= p[3]

    def p_boolean_gte(self, p):
        'boolean: factor GTE factor'
        p[0] = p[1] >= p[3]

    def p_factor_var(self, p):
        'factor: VAR'
        p[0] = p[1]

    def p_factor_int(self, p):
        'factor: INT'
        p[0] = p[1]

    def p_factor_decimal(self, p):
        'factor: DECIMAL'
        p[0] = p[1]

    def p_negative_factor(self, p):
        'factor: MINUS factor'
        p[0] = -p[2]
