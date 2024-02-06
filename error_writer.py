import os

class ErrorWriter:
    _general_output = "all_errors.txt"
    _duplicate_output = "duplicates.txt"

    @classmethod
    def write_duplicate_error(cls, file_path, line_num, duplicate_string):
        with open(cls._duplicate_output, 'a', encoding='utf-8') as duplicate:
            duplicate.write("===========================================================================\n")
            duplicate.write(f"Error in {os.path.basename(file_path)}, around line {line_num}:\n")
            duplicate.write(f"Description: Duplicate string found\n")
            duplicate.write(f"Original: '{duplicate_string}'\n")
            duplicate.write("===========================================================================\n\n")

    @classmethod
    def write_error(cls, error: str):
        with open(cls._general_output, 'a', encoding='utf-8') as output:
            output.write(error)

    @staticmethod
    def reset_error_files():
        with open(ErrorWriter._general_output, 'w', encoding='utf-8'):
            pass
        with open(ErrorWriter._duplicate_output, 'w', encoding='utf-8'):
            pass
