from evaluator import BooleanParser

parser = BooleanParser()


def test_comparison_1():
    assert parser.parse('1==1') == True


def test_comparison_2():
    assert parser.parse('3<2') == False
