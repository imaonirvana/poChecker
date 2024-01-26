import os

class ErrorWriter:
    @staticmethod
    def write_duplicate_error(output_file, file_path, line_num, duplicate_string, duplicate_file):
        with open(output_file, 'a', encoding='utf-8') as output:
            output.write("===========================================================================\n")
            output.write(f"Error in {os.path.basename(file_path)}, line {line_num}:\n")
            output.write(f"Description: Duplicate string found\n")
            output.write(f"Original: '{duplicate_string}'\n")
            output.write("===========================================================================\n\n")

        with open(duplicate_file, 'a', encoding='utf-8') as duplicate:
            duplicate.write("===========================================================================\n")
            duplicate.write(f"Error in {os.path.basename(file_path)}, line {line_num}:\n")
            duplicate.write(f"Description: Duplicate string found\n")
            duplicate.write(f"Original: '{duplicate_string}'\n")
            duplicate.write("===========================================================================\n\n")

    @staticmethod
    def write_error(output_file, file_path, line_num, description, original, translated=None):
        with open(output_file, 'a', encoding='utf-8') as output:
            output.write("===========================================================================\n")
            output.write(f"Error in {os.path.basename(file_path)}, line {line_num}:\n")
            output.write(f"Description: {description}\n")
            output.write(f"Original: '{original}'\n")
            if translated is not None:
                output.write(f"Translated: '{translated}'\n")
            output.write("===========================================================================\n\n")
