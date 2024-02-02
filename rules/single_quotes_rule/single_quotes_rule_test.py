from rules.single_quotes_rule.single_quotes_rule import SingleQuotesRule


def test_should_dont_change_anything():
    original = 'Test some original'
    translated = "Some translated"

    assert SingleQuotesRule().fix_translation(original, translated) == translated

    pass


def test_should_change_to_apostrophe():
    original = 'Test some original'
    translated = "Some v'alue tr'anslated"

    assert SingleQuotesRule().fix_translation(original, translated) == "Some v`alue tr`anslated"

    pass


def test_should_dont_change_near_special_symbols():
    original = 'Test some original'
    translated = "Some value 'translated'."

    assert SingleQuotesRule().fix_translation(original, translated) == "Some value 'translated'."

    pass


def test_should_dont_change_free_quotes():
    original = 'Test some original'
    translated = "Some value ' translated '"

    assert SingleQuotesRule().fix_translation(original, translated) == "Some value ' translated '"

    pass


def test_should_say_it_valid():
    assert not SingleQuotesRule().is_broken('Test some original', "'Some' translated")
    assert not SingleQuotesRule().is_broken("Test some original", "Some ''' translated'.")
    assert not SingleQuotesRule().is_broken('Test some original', "Some %!'#% translated")


def test_should_say_it_invalid():
    assert SingleQuotesRule().is_broken('Test some original', "So'me tran'slat'ed")
    assert SingleQuotesRule().is_broken('Test some original', "S'o'me tr21'anslated")
