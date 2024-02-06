import polib

from PipelineInput import PipelineInput
from error_writer import ErrorWriter
from ignore_phrases import ignore_phrases
from output_writers.output_writer import OutputWriter
from pipe_line import Pipeline


class StringChecker:
    @staticmethod
    def check_po_file(file_path):
        try:
            po = polib.pofile(file_path)
            output_writer = OutputWriter(file_path)

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
                        pipeline_input = PipelineInput(original_string, translated_string, file_path, entry.linenum)
                        StringChecker.check_string_rules(pipeline_input, output_writer)

                except Exception as inner_exception:
                    print(inner_exception)

            output_writer.flush()

        except Exception as outer_exception:
            print(outer_exception)

    @staticmethod
    def check_string_rules(pipeline_input: PipelineInput, output_writer: OutputWriter):
        pipe_line = Pipeline()

        if not pipe_line.is_broken(pipeline_input.get_original(), pipeline_input.get_translated()):
            return

        fixed_translation = pipe_line.process_translation(pipeline_input)
        output_writer.write_to_line(fixed_translation, pipeline_input.get_line_num())
