import polib

from PipelineInput import PipelineInput
from error_writer import ErrorWriter
from ignore_phrases import ignore_phrases
from output_writers.output_writer import OutputWriter
from pipe_line import Pipeline

class StringChecker:
    @staticmethod
    def check_po_file(file_path):
        """
        Обробляє .po файл за певними правилами та повертає список знайдених помилок.
        """
        errors_list = []
        try:
            try:
                po = polib.pofile(file_path)
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError for {file_path}: {e}. Trying cp1251 encoding.")
                po = polib.pofile(file_path, encoding='cp1251')
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
                        # Викликаємо існуючу логіку для виведення дубліката
                        ErrorWriter.write_duplicate_error(file_path, entry.linenum, original_string)
                        errors_list.append({
                            'file_name': file_path,
                            'line_number': entry.linenum,
                            'error_description': 'Duplicate entry: original equals translated or duplicate found.',
                            'original': original_string,
                            'translated': translated_string
                        })
                    else:
                        seen_entries[key] = True

                    if translated_string:
                        pipeline_input = PipelineInput(original_string, translated_string, file_path, entry.linenum)
                        # Передаємо file_path як окремий параметр
                        StringChecker.check_string_rules(pipeline_input, output_writer, errors_list, file_path)

                except Exception as inner_exception:
                    print(inner_exception)
                    errors_list.append({
                        'file_name': file_path,
                        'line_number': entry.linenum,
                        'error_description': 'Exception in entry processing: ' + str(inner_exception),
                        'original': entry.msgid,
                        'translated': entry.msgstr
                    })

            output_writer.flush()

        except Exception as outer_exception:
            print(outer_exception)
            errors_list.append({
                'file_name': file_path,
                'line_number': 0,
                'error_description': 'Exception in file processing: ' + str(outer_exception),
                'original': '',
                'translated': ''
            })

        return errors_list

    @staticmethod
    def check_string_rules(pipeline_input: PipelineInput, output_writer, errors_list, file_path):
        """
        Перевіряє рядки за допомогою Pipeline. Якщо правило не пройдене, виконується коригування
        та запис у output, а також додається запис у список помилок.
        """
        pipe_line = Pipeline()

        if not pipe_line.is_broken(pipeline_input.get_original(), pipeline_input.get_translated()):
            return

        fixed_translation = pipe_line.process_translation(pipeline_input)
        output_writer.write_to_line(fixed_translation, pipeline_input.get_line_num())
        errors_list.append({
            'file_name': file_path,
            'line_number': pipeline_input.get_line_num(),
            'error_description': 'String failed rule checks; fixed translation applied.',
            'original': pipeline_input.get_original(),
            'translated': pipeline_input.get_translated()
        })
