import ply.yacc as yacc
from .questionTokenizer import tokens, question_lexer
from .exceptions import ParserSyntaxError, ParserVariableNotFound
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().rounding = ROUND_HALF_UP


class QuestionParser:
    def __init__(self, **kwargs):
        self.table = kwargs
        self.tokens = tokens
        self.parser = yacc.yacc(module=self, tabmodule='questionParseTab')

    def parse(self, s: str) -> str:
        return self.parser.parse(s, lexer=question_lexer.clone())

    def p_text_expression(self, p):
        'text : text START expression RPAREN text'
        p[0] = (p[1] if p[1] else '') + str(p[3]) + (p[5] if p[5] else '')

    def p_text_char_text(self, p):
        'text : CHAR text'
        p[0] = p[1] + p[2]

    def p_text_char(self, p):
        'text : CHAR'
        p[0] = p[1]

    def p_text_empty(self, p):
        'text :'
        pass

    def p_expression_plus(self, p):
        'expression : expression PLUS term'
        p[0] = p[1] + p[3]

    def p_expression_minus(self, p):
        'expression : expression MINUS term'
        p[0] = p[1] - p[3]

    def p_expresion_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_term_exponent(self, p):
        'factor : factor EXP factor'
        p[0] = p[1]**p[3]

    def p_term_times(self, p):
        'term : term TIMES factor'
        p[0] = p[1] * p[3]

    def p_term_divide(self, p):
        'term : term DIVIDE factor'
        a = p[1]
        b = p[3]
        remainder = a % b
        if isinstance(a, int) and isinstance(b, int) and remainder == 0:
            result = a // b
        else:
            result = Decimal(a) / Decimal(b)
        p[0] = result

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]

    def p_factor_negative(self, p):
        'factor : MINUS factor'
        p[0] = -p[2]

    def p_factor_int(self, p):
        'factor : INT'
        p[0] = p[1]

    def p_factor_decimal(self, p):
        'factor : DECIMAL'
        p[0] = p[1]

    def p_factor_var(self, p):
        'factor : VAR'
        if p[1] not in self.table:
            raise ParserVariableNotFound
        p[0] = self.table[p[1]]

    def p_factor_expression(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_error(self, p):
        raise ParserSyntaxError("Syntax Error")
