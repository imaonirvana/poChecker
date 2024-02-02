from rules.tilde_rule.tilde_rule import TildeRule


def test_should_dont_change_anything():
    original = 'Test some original'
    translated = 'Some translated'

    assert TildeRule().fix_translation(original, translated) == translated

    pass


def test_should_retain_brackets():
    original = 'Test some ~should_retain~ original'
    translated = 'Some ~changed~ translated'

    assert TildeRule().fix_translation(original, translated) == 'Some ~should_retain~ translated'

    pass


def test_should_retain_multiple_brackets():
    original = 'Test some ~should_retain~ original ~should_retain_2~'
    translated = 'Some ~changed~ translated ~changed_2~'
    fixed = TildeRule().fix_translation(original, translated)

    assert fixed == 'Some ~should_retain~ translated ~should_retain_2~'

    pass


def test_should_compare_in_one():
    original = 'Test some ~should_retain~ original ~should_retain~'
    translated = 'Some ~should_retain~'

    assert TildeRule().fix_translation(original, translated) == translated

    pass


def test_should_say_it_valid():

    assert not TildeRule().is_broken('Test some original', 'Some translated')
    assert not TildeRule().is_broken('Test ~should_retain~ some original', 'Some translated')
    assert not TildeRule().is_broken('Test ~should_retain~ some original', 'Some ~should_retain~ translated')


def test_should_say_it_invalid():
    original = 'Test some ~should_retain~ original'
    translated = 'Some ~changed~ translated'

    assert TildeRule().is_broken(original, translated)
