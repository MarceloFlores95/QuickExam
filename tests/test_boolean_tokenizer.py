from evaluator import boolean_lexer


def string_to_tokens(s: str):
    lex = boolean_lexer.clone()
    lex.input(s)
    return [(t.type, t.value) for t in lex]


def test_or():
    assert string_to_tokens('|or||OR') == [('OR', '|'), ('OR', 'or'),
                                           ('OR', '||'), ('OR', 'OR')]


def test_and():
    assert string_to_tokens('&and&&AND') == [('AND', '&'), ('AND', 'and'),
                                             ('AND', '&&'), ('AND', 'AND')]


def test_true():
    assert string_to_tokens('1trueTrue') == [('TRUE', True), ('TRUE', True),
                                             ('TRUE', True)]


def test_false():
    assert string_to_tokens('0falseFalse') == [('FALSE', False),
                                               ('FALSE', False),
                                               ('FALSE', False)]


def test_variable():
    assert string_to_tokens('a or b') == [('VAR', 'a'), ('OR', 'or'),
                                          ('VAR', 'b')]


def test_not():
    assert string_to_tokens('~b') == [('NOT', '~'), ('VAR', 'b')]
