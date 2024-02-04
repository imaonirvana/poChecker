from rules.odd_quotes_rule.odd_quotes_rule import OddQuotesRule


def test_should_dont_change_anything():
    original = 'Test some original'
    translated = 'Some translated'

    assert OddQuotesRule().fix_translation(original, translated) == translated

    pass

def test_should_say_it_valid():

    assert not OddQuotesRule().is_broken("test some original", "Some 'translated'")
    assert not OddQuotesRule().is_broken('test some original', "2Some tran'sla'ted")


def test_should_say_it_invalid():
    assert OddQuotesRule().is_broken('test some original', "S'ome tr'ansl'ated")
    assert OddQuotesRule().is_broken('Test some original', "s'om'e ' 'translat'ed")
