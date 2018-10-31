class ParserException(Exception):
    pass


class ParserSyntaxError(ParserException):
    pass


class ParserVariableNotFound(ParserException):
    pass


class LexerException(Exception):
    pass


class LexerInvalidToken(LexerException):
    pass
