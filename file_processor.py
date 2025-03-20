import os
from string_checker import StringChecker


def process_po_files(directory):
    """
    Обробляє всі .po файли в заданій директорії.
    Повертає кортеж: (total_files, total_errors, files_data)
      де files_data – список словників:
         {
           'file_name': ...,
           'file_path': ...,
           'errors': [список помилок]
         }
    """
    files_data = []
    total_files = 0
    total_errors = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.po'):
                total_files += 1
                file_path = os.path.join(root, file)
                errors = StringChecker.check_po_file(file_path)
                total_errors += len(errors)
                files_data.append({
                    'file_name': file,
                    'file_path': file_path,
                    'errors': errors
                })

    return total_files, total_errors, files_data
