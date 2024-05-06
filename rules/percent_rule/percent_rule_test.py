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


def test_should_not_change_end_of_string():
    original = 'Test some %should_retain?'
    translated = 'Some %changed translated'

    assert PercentRule().fix_translation(original, translated) == 'Some %should_retain translated'

    pass


def test_should_change_multy_variables_correctly():
    original = 'Zone (%d) %s(%s) is out of bound (%d..%d)'
    translated = 'Зоната %changed_1 %changed_2 %changed_4 е извън обхвата %changed_3'

    assert PercentRule().fix_translation(original, translated) == 'Зоната (%d) %s(%s) (%d..%d) е извън обхвата %changed_3'

    pass


def test_should_change_multiple_percents():
    original = 'Zone 75%% full'
    translated = 'Зона 75%% повна'

    assert PercentRule().fix_translation(original, translated) == translated

    pass


def test_should_change_variables_in_any_brackets():
    original = 'Zone %{value} [%s] is out of bound (%s) #%s" %(minimum)d'
    translated = 'Зоната %changed_1 е извън обхвата %changed_2 %changed_3 %changed_4 %changed_5'

    assert PercentRule().fix_translation(original, translated) == 'Зоната %{value} е извън обхвата [%s] (%s) %s %(minimum)d'

    pass


def test_should_change_variables_with_special_characters_correctly():
    original = 'Stopped runner %runner_ids->type|uniq% for panels %runner_ids->serial%'
    translated = 'Спрян изпълнител %changed% за панели %changed2%'

    assert PercentRule().fix_translation(original,
                                         translated) == 'Спрян изпълнител %runner_ids->type|uniq% за панели %runner_ids->serial%'

    pass


def test_should_compare_in_one():
    original = 'Test some %should_retain% original %should_retain%'
    translated = 'Some %should_retain%'

    assert PercentRule().fix_translation(original, translated) == translated

    pass


def test_should_say_it_valid():

    assert not PercentRule().is_broken('Test some original', 'Some translated')
    assert not PercentRule().is_broken('Test %should_retain some original', 'Some %should_retain translated')
    assert not PercentRule().is_broken('Test %should_retain% some original', 'Some %should_retain% translated')
    assert not PercentRule().is_broken('Test %should_retain% some original %sh2% as', 'Some %sh2% saasas %should_retain% translated')


def test_should_say_it_invalid():

    assert PercentRule().is_broken('Test some %should_retain% original', 'Some %changed% translated')
    assert PercentRule().is_broken('Test some %should_retain original', 'Some %changed translated')
