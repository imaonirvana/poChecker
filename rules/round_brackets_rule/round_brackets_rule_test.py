from rules.round_brackets_rule.round_brackets_rule import RoundBracketsRule


def test_should_dont_change_anything():
    original = 'Test some original'
    translated = 'Some translated'

    assert RoundBracketsRule().fix_translation(original, translated) == translated

    pass


def test_should_retain_brackets():
    original = 'Test some $(should_retain) original'
    translated = 'Some $(changed) translated'

    assert RoundBracketsRule().fix_translation(original, translated) == 'Some $(should_retain) translated'

    pass


def test_should_retain_multiple_brackets():
    original = 'Test some $(should_retain) original $(should_retain_2)'
    translated = 'Some $(changed) translated $(changed_2)'
    fixed = RoundBracketsRule().fix_translation(original, translated)

    assert fixed == 'Some $(should_retain) translated $(should_retain_2)'

    pass


def test_should_compare_in_one():
    original = 'Test some $(should_retain) original $(should_retain)'
    translated = 'Some $(should_retain)'

    assert RoundBracketsRule().fix_translation(original, translated) == translated

    pass


def test_should_say_it_valid():

    assert not RoundBracketsRule().is_broken('Test some original', 'Some translated')
    assert not RoundBracketsRule().is_broken('Test $(should_retain) some original', 'Some translated $(should_retain)')
    assert not RoundBracketsRule().is_broken('Test $(should_retain) some original $(should_retain2)', 'Some translated $(should_retain2) ASSAA $(should_retain) asassa')


def test_should_say_it_invalid():
    original = 'Test some $(should_retain) original'
    translated = 'Some $(changed) translated'

    assert RoundBracketsRule().is_broken(original, translated)

def test_should_not_contain_forbiden_chars():
    original = 'Test some $(should_retain) original'
    translated = 'Some $(j) translated $(k + 1)'

    assert RoundBracketsRule().fix_translation(original, translated) == translated
