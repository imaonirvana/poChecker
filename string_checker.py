import re
import polib
from error_writer import ErrorWriter
from ignore_phrases import ignore_phrases
from output_writer.output_writer import OutputWriter
from pipe_line import Pipeline


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
        output_writer = OutputWriter(file_path)
        pipe_line = Pipeline(file_path, line_num)

        if not pipe_line.is_broken(original, translated):
            return

        fixed_translation = pipe_line.process_translation(original, translated)
        output_writer.write_to_line(fixed_translation, line_num)