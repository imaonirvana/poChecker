from file_processor import FileProcessor
from string_checker import StringChecker

import os

if __name__ == "__main__":
    po_files = ["frontend.po", "xml.po", "apps.po", "api.po", "interactive.po", "rest-api.po", "mmisvc.po"]
    output_file = "error_output.txt"

    with open(output_file, 'w', encoding='utf-8'):
        pass

    for po_file in po_files:
        file_path = os.path.join(r"C:\Users\dfun8\Desktop\delta_files\el_GR.UTF-8", po_file)

        print(f"Processing file: {file_path}")

        FileProcessor.convert_line_endings_to_unix(file_path)
        StringChecker.check_po_file(file_path, output_file)

    print("Done checking files!")
