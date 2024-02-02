from rules.capitalization_rule.capitalization_rule import CapitalizationRule


def test_should_dont_change_anything():
    original = 'Test some original'
    translated = 'Some translated'

    assert CapitalizationRule().fix_translation(original, translated) == translated

    pass

def test_should_say_it_valid():

    assert not CapitalizationRule().is_broken('2test some original', 'Some translated')
    assert not CapitalizationRule().is_broken('test some original', '2Some translated')
    assert not CapitalizationRule().is_broken('- Test some original', '+ some translated')


def test_should_say_it_invalid():
    assert CapitalizationRule().is_broken('test some original', 'Some translated')
    assert CapitalizationRule().is_broken('Test some original', 'some translated')
