from rules.double_quotes_rule.double_quotes_rule import DoubleQuotesRule


def test_should_dont_change_anything():
    original = 'Test some original'
    translated = "Some 'translated'"

    assert DoubleQuotesRule().fix_translation(original, translated) == translated

    pass


def test_should_change_to_single_quotes():
    original = 'Test some "original"'
    translated = 'Some "value" translated'

    assert DoubleQuotesRule().fix_translation(original, translated) == "Some 'value' translated"

    pass


def test_should_change_one_double_to_single():
    original = 'Test some "original'
    translated = 'Some value" translated'

    assert DoubleQuotesRule().fix_translation(original, translated) == "Some value' translated"

    pass


def test_should_say_it_valid():
    assert not DoubleQuotesRule().is_broken('2test some original', 'Some translated')
    assert not DoubleQuotesRule().is_broken("test some original", "2Some 'translated'")
    assert not DoubleQuotesRule().is_broken('- Test "some" original', "some translated")


def test_should_say_it_invalid():
    assert DoubleQuotesRule().is_broken('test some original', 'Some "translated"')
    assert DoubleQuotesRule().is_broken('Test some original', 'some tr(%"21anslated')
