#!/usr/bin/env python3
import argparse
import db
from file_processor import FileProcessor

def main():
    parser = argparse.ArgumentParser(description='Запуск poChecker для перевірки .po файлів')
    parser.add_argument('-path', required=True, help='Шлях до каталогу з .po файлами')
    parser.add_argument('--use-db', action='store_true', help='Зберігати результати у базу даних')
    args = parser.parse_args()

    directory = args.path

    if args.use_db:
        db.init_db()

    total_files, total_errors, errors_list = FileProcessor.process_po_files(directory)

    # Запис результатів у текстовий файл (залишаємо існуючу логіку)
    with open('all_errors.txt', 'w', encoding='utf-8') as f:
        for error in errors_list:
            f.write("====================================\n")
            f.write("Error in {} line {}:\n".format(error.get('file_name'), error.get('line_number')))
            f.write("Description: {}\n".format(error.get('error_description')))
            f.write("Original: {}\n".format(error.get('original')))
            f.write("Translated: {}\n".format(error.get('translated', '')))
            f.write("====================================\n\n")

    if args.use_db:
        run_data = {
            'directory': directory,
            'total_files': total_files,
            'total_errors': total_errors
        }
        db.save_run(run_data, errors_list)
        print("Результати збережено у базу даних.")

if __name__ == '__main__':
    main()
