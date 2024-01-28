from fix_translations import FixTranslations


def test_should_dont_change_anything():
    original = 'Test some original'
    translated = 'Some translated'

    assert FixTranslations.fix_translation(original, translated) == translated

    pass


def test_should_retain_brackets():
    original = 'Test some $(should_retain) original'
    translated = 'Some $(changed) translated'

    assert FixTranslations.fix_translation(original, translated) == 'Some $(should_retain) translated'

    pass


def test_should_retain_multiple_brackets():
    original = 'Test some $(should_retain) original $(should_retain_2)'
    translated = 'Some $(changed) translated $(changed_2)'
    fixed = FixTranslations.fix_translation(original, translated)

    assert fixed == 'Some $(should_retain) translated $(should_retain_2)'

    pass


def test_should_say_it_valid():

    assert not FixTranslations.is_broken('Test some original', 'Some translated')
    assert not FixTranslations.is_broken('Test $(should_retain) some original', 'Some translated')


def test_should_say_it_invalid():
    original = 'Test some $(should_retain) original'
    translated = 'Some $(changed) translated'

    assert FixTranslations.is_broken(original, translated)

