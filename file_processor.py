import os
import io
from string_checker import StringChecker

class FileProcessor:
    @staticmethod
    def convert_line_endings_to_unix(file_path):
        try:
            with io.open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            content = content.replace('\r\n', '\n').replace('\r', '\n')

            with io.open(file_path, 'w', encoding='utf-8', newline='\n') as file:
                file.write(content)

        except FileNotFoundError:
            print(f"File not found: {file_path}. Skipping...")

    @staticmethod
    def process_po_files(directory):
        """
        Обробляє всі .po файли в заданій директорії.
        Повертає кортеж: (total_files, total_errors, aggregated_errors)
        """
        total_files = 0
        aggregated_errors = []

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.po'):
                    total_files += 1
                    file_path = os.path.join(root, file)
                    errors = StringChecker.check_po_file(file_path)
                    aggregated_errors.extend(errors)

        return total_files, len(aggregated_errors), aggregated_errors
