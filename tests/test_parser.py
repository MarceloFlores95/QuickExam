from ExpressionEvaluator import Parser


def test_factor():
    assert Parser().parse('3') == '3'


def test_sum():
    assert Parser().parse('$(3+5)$') == '8'


def test_ambiguity_1():
    assert Parser().parse('$(3+4*5)$') == '23'


def test_variables():
    assert Parser(a=1, b=5).parse('$(a+b)$') == '6'


def test_with_text():
    assert Parser().parse('2+2=$(2+2)$') == '2+2=4'


def test_with_text_2():
    assert Parser(
        name='Juan').parse('Hola $(name)$ 2+2=$(2+2)$') == 'Hola Juan 2+2=4'
