from rules.percent_rule.percent_rule import PercentRule


def test_should_dont_change_anything():
    original = 'Test some original'
    translated = 'Some translated'

    assert PercentRule().fix_translation(original, translated) == translated

    pass


def test_should_retain_one_percent():
    original = 'Test some %should_retain original'
    translated = 'Some %changed translated'

    assert PercentRule().fix_translation(original, translated) == 'Some %should_retain translated'

    pass


def test_should_retain_two_percent():
    original = 'Test some %should_retain% original'
    translated = 'Some %changed% translated'

    assert PercentRule().fix_translation(original, translated) == 'Some %should_retain% translated'

    pass


def test_should_retain_multiple_percents():
    original = 'Test some %should_retain original %should_retain_2%'
    translated = 'Some %changed translated %changed_2%'
    fixed = PercentRule().fix_translation(original, translated)

    assert fixed == 'Some %should_retain translated %should_retain_2%'

    pass


def test_should_compare_in_one():
    original = 'Test some %should_retain% original %should_retain%'
    translated = 'Some %should_retain%'

    assert PercentRule().fix_translation(original, translated) == translated

    pass


def test_should_say_it_valid():

    assert not PercentRule().is_broken('Test some original', 'Some translated')
    assert not PercentRule().is_broken('Test %should_retain% some original', 'Some translated')
    assert not PercentRule().is_broken('Test %should_retain some original', 'Some %should_retain translated')
    assert not PercentRule().is_broken('Test %should_retain% some original', 'Some %should_retain% translated')


def test_should_say_it_invalid():

    assert PercentRule().is_broken('Test some %should_retain% original', 'Some %changed% translated')
    assert PercentRule().is_broken('Test some %should_retain original', 'Some %changed translated')
