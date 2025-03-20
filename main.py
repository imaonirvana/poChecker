#!/usr/bin/env python3
import argparse
import db
from file_processor import process_po_files

def main():
    parser = argparse.ArgumentParser(description='Запуск poChecker для перевірки .po файлів')
    parser.add_argument('-path', required=True, help='Шлях до каталогу з .po файлами')
    parser.add_argument('--use-db', action='store_true', help='Зберігати результати у базу даних')
    args = parser.parse_args()

    directory = args.path

    if args.use_db:
        db.init_db()  # Створює (якщо треба) таблиці та заповнює rules/error_types

    total_files, total_errors, files_data = process_po_files(directory)

    # Запис результатів у текстовий файл (існуюча логіка)
    with open('all_errors.txt', 'w', encoding='utf-8') as f:
        for file_info in files_data:
            file_path = file_info.get('file_path')
            for error in file_info.get('errors', []):
                f.write("====================================\n")
                f.write("Error in {} line {}:\n".format(file_path, error.get('line_number')))
                f.write("Description: {}\n".format(error.get('error_description')))
                f.write("Original: {}\n".format(error.get('original')))
                f.write("Translated: {}\n".format(error.get('translated', '')))
                f.write("Rule: {}\n".format(error.get('rule', '')))
                f.write("====================================\n\n")

    # Якщо потрібно зберегти у БД
    if args.use_db:
        run_data = {
            'directory': directory,
            'total_files': total_files,
            'total_errors': total_errors
        }
        db.save_run_full(run_data, files_data)
        print("Результати збережено у базу даних.")

if __name__ == '__main__':
    main()
