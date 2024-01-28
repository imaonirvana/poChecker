import argparse
from file_processor import FileProcessor
from string_checker import StringChecker
from error_writer import ErrorWriter
import os

def main():
    parser = argparse.ArgumentParser(description="Process PO files and check for errors.")
    parser.add_argument("-path", dest="directory_path", help="Path to the directory containing PO files")

    args = parser.parse_args()

    if not args.directory_path:
        print("Error: Please provide the path to the directory using the -path argument.")
        return

    po_files = ["frontend.po", "xml.po", "apps.po", "api.po", "interactive.po", "rest-api.po", "mmisvc.po"]

    ErrorWriter.reset_error_files()

    for po_file in po_files:
        file_path = os.path.join(args.directory_path, po_file)

        print(f"Processing file: {file_path}")

        FileProcessor.convert_line_endings_to_unix(file_path)
        StringChecker.check_po_file(file_path)

    print("Done checking files!")

if __name__ == "__main__":
    main()
