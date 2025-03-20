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

                    # Перевірка на дублікат
                    key = (original_string, translated_string, entry.linenum)
                    if original_string in ignore_phrases:
                        continue

                    if (original_string == translated_string and not original_string.isdigit()) or key in seen_entries:
                        ErrorWriter.write_duplicate_error(file_path, entry.linenum, original_string)
                        errors_list.append({
                            'line_number': entry.linenum,
                            'error_description': 'Duplicate entry: original equals translated or duplicate found.',
                            'original': original_string,
                            'translated': translated_string,
                            'rule': 'duplicate_rule'  # <- назва правила для дубліката
                        })
                    else:
                        seen_entries[key] = True

                    # Перевірка інших правил (наприклад, capitalization_rule)
                    if translated_string:
                        pipeline_input = PipelineInput(original_string, translated_string, file_path, entry.linenum)
                        StringChecker.check_string_rules(pipeline_input, output_writer, errors_list)

                except Exception as inner_exception:
                    print(inner_exception)
                    errors_list.append({
                        'line_number': entry.linenum,
                        'error_description': 'Exception in entry processing: ' + str(inner_exception),
                        'original': entry.msgid,
                        'translated': entry.msgstr,
                        'rule': 'exception_rule'
                    })

            output_writer.flush()

        except Exception as outer_exception:
            print(outer_exception)
            errors_list.append({
                'line_number': 0,
                'error_description': 'Exception in file processing: ' + str(outer_exception),
                'original': '',
                'translated': '',
                'rule': 'exception_rule'
            })

        return errors_list

    @staticmethod
    def check_string_rules(pipeline_input: PipelineInput, output_writer, errors_list):
        """
        Тут можна перевіряти інші правила (capitalization_rule, double_quotes_rule тощо).
        Для прикладу, використаємо "capitalization_rule" – перевірку першої великої літери.
        """
        pipe_line = Pipeline()
        original = pipeline_input.get_original()
        translated = pipeline_input.get_translated()

        # Наприклад, перевірка на велику літеру в перекладі (capitalization_rule)
        if translated and len(translated) > 0:
            # Якщо переклад не починається з великої літери, вважаємо це помилкою
            if translated[0].islower():
                output_writer.write_to_line(
                    f"Auto-correction for capitalization: {translated.capitalize()}",
                    pipeline_input.get_line_num()
                )
                errors_list.append({
                    'line_number': pipeline_input.get_line_num(),
                    'error_description': 'Translation does not start with a capital letter.',
                    'original': original,
                    'translated': translated,
                    'rule': 'capitalization_rule'
                })

        # Приклад виклику pipeline
        if pipe_line.is_broken(original, translated):
            fixed_translation = pipe_line.process_translation(pipeline_input)
            output_writer.write_to_line(fixed_translation, pipeline_input.get_line_num())
            errors_list.append({
                'line_number': pipeline_input.get_line_num(),
                'error_description': 'String failed pipeline checks; fixed translation applied.',
                'original': original,
                'translated': translated,
                'rule': 'exception_rule'  # або 'some_other_rule'
            })
