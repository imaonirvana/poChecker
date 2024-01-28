import re
import polib
from error_writer import ErrorWriter
from ignore_phrases import ignore_phrases
from fix_translations.fix_translations import FixTranslations


class StringChecker:
    @staticmethod
    def check_po_file(file_path):
        try:
            po = polib.pofile(file_path)
            seen_entries = {}

            for entry in po:
                try:
                    original_string = entry.msgid
                    translated_string = entry.msgstr

                    if not original_string:
                        continue

                    key = (original_string, translated_string, entry.linenum)

                    if original_string in ignore_phrases:
                        continue

                    if (original_string == translated_string and not original_string.isdigit()) or key in seen_entries:
                        ErrorWriter.write_duplicate_error(file_path, entry.linenum, original_string)
                    else:
                        seen_entries[key] = True

                    if translated_string:
                        StringChecker.check_string_rules(original_string, translated_string, file_path, entry.linenum)

                except Exception as inner_exception:
                    ErrorWriter.write_error(file_path, entry.linenum, "Error processing entry",
                                            str(inner_exception))

        except Exception as outer_exception:
            ErrorWriter.write_error(file_path, 0, "Error processing file", str(outer_exception))

    @staticmethod
    def check_string_rules(original, translated, file_path, line_num):

        # Rule 1: Check capital letters in the first character, excluding numbers and symbols
        if (original and original[0].isalpha() and translated and translated[0].isalpha() and
                ((original[0].isupper() and translated[0].islower()) or
                 (original[0].islower() and translated[0].isupper()))):
            ErrorWriter.write_error(file_path, line_num, "Capitalization mismatch", original, translated)

        # Rule 2: Check single quotes in the translated string
        single_quotes_translated = translated.count("'")

        if single_quotes_translated % 2 == 1:
            ErrorWriter.write_error(file_path, line_num, "Odd number of single quotes", original, translated)

        # Rule 3: Check % translation
        original_pattern = re.compile(r'(?<!%)%(\S*?)%')
        translated_pattern = re.compile(r'(?<!%)%(\S*?)%')

        original_matches = set(original_pattern.findall(original))
        translated_matches = set(translated_pattern.findall(translated))

        if original_matches != translated_matches:
            ErrorWriter.write_error(file_path, line_num, "% translation mismatch", original, translated)

        # Rule 4: Check tilde translation
        if '~' in original and '~' in translated:
            ErrorWriter.write_error(file_path, line_num, "Tilde translation found", original, translated)

        # Rule 5: Do not translate words inside the "round brackets" and with $ before them
        pattern = r'\$\([^\)]+\)'

        original_matches = re.findall(pattern, original)
        translated_matches = re.findall(pattern, translated)

        if original_matches != translated_matches:
            ErrorWriter.write_error(file_path, line_num, "Round bracket and $ translation mismatch", original,
                                    translated)
            FixTranslations.fix_translation(original, translated)

        # Rule 6: Check double quotes, excluding those within square brackets
        if '"' in translated and not re.search(r'\[[^\]]*"[^\]]*"\]', original, re.IGNORECASE):
            ErrorWriter.write_error(file_path, line_num,
                                    "Double quotes should be replaced with single quotes",
                                    original, translated)
