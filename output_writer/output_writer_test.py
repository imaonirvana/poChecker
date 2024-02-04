from output_writer import OutputWriter

output_writer = OutputWriter("/any/path")
lines = [
    '#: application/modules/ipmp/models/Rest/Form/User/Remove.php:43',
    'msgid "Cannot remove current user"',
    'msgstr "Aktuálního uživatele nelze smazat"',
    '',
    '#: application/modules/ipmp/models/Rest/Form/User/Forgot.php:34',
    '#: application/modules/ipmp/models/Form/LoginForm.php:47',
    'msgid "User not found"',
    'msgstr "Uživatel nenalezen"',
    '#: src/components/Panel/CustomerMap.js:27',
    'msgid ""',
    '"There is a problem with the Google API key. Please contact to PowerManage "',
    '"administrator."',
    'msgstr ""',
    '"S Google API klíčem je problém. Obraťte se prosím na správce PowerManage."',
]


def test_should_return_valid_index_range_for_one_line():
    result = output_writer.get_translated_text_range(lines, 1)

    assert result[0] == 2
    assert result[1] == 2

    pass


def test_should_return_valid_index_range_for_multiple_line():
    result = output_writer.get_translated_text_range(lines, 9)

    assert result[0] == 12
    assert result[1] == 13

    pass


def test_should_return_valid_index_range_for_empty_line():
    result = output_writer.get_translated_text_range(lines, 123123)

    assert result[0] == -1
    assert result[1] == -1

    pass

def test_should_append_right_prefix():
    escaped = output_writer.escape_content_value("Some content")

    assert escaped.startswith("msgstr")
    pass