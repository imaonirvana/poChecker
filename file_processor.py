import os
import io
from string_checker import StringChecker

class FileProcessor:
    @staticmethod
    def convert_line_endings_to_unix(file_path):
        with io.open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        content = content.replace('\r\n', '\n').replace('\r', '\n')

        with io.open(file_path, 'w', encoding='utf-8', newline='\n') as file:
            file.write(content)

    @staticmethod
    def process_po_files(directory, output_file):
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.po'):
                    file_path = os.path.join(root, file_name)
                    print(f"Processing file: {file_path}")

                    with io.open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()

                    if '\r\n' in content or '\r' in content:
                        FileProcessor.convert_line_endings_to_unix(file_path)

                    StringChecker.check_po_file(file_path, output_file)
