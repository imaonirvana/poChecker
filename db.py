import sqlite3
import os
from datetime import datetime


def init_db(db_path='poChecker.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Таблиця roles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT UNIQUE,
            role_description TEXT
        )
    ''')

    # 2. Таблиця users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role_id INTEGER,
            FOREIGN KEY(role_id) REFERENCES roles(role_id)
        )
    ''')

    # 3. Таблиця runs (додано result_file)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date TEXT,
            directory TEXT,
            total_files INTEGER,
            total_errors INTEGER,
            user_id INTEGER,
            result_file TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    # 4. Таблиця files
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            file_name TEXT,
            file_path TEXT,
            FOREIGN KEY(run_id) REFERENCES runs(run_id)
        )
    ''')

    # 5. Таблиця rules
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT UNIQUE,
            rule_description TEXT
        )
    ''')

    # 6. Таблиця error_types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_types (
            error_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_type_name TEXT,
            error_type_description TEXT
        )
    ''')

    # 7. Таблиця errors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS errors (
            error_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER,
            rule_id INTEGER,
            error_type_id INTEGER,
            line_number INTEGER,
            error_description TEXT,
            original TEXT,
            translated TEXT,
            FOREIGN KEY(file_id) REFERENCES files(file_id),
            FOREIGN KEY(rule_id) REFERENCES rules(rule_id),
            FOREIGN KEY(error_type_id) REFERENCES error_types(error_type_id)
        )
    ''')

    conn.commit()
    populate_static_data(cursor)
    conn.commit()
    conn.close()

def get_db_connection(db_path='poChecker.db'):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def populate_static_data(cursor):
    # Заповнення таблиці roles
    roles_data = [
        ('user', 'Звичайний користувач, може бачити лише власні запуски'),
        ('moderator', 'Модератор, може бачити всі запуски')
    ]
    for role_name, role_desc in roles_data:
        cursor.execute("SELECT COUNT(*) FROM roles WHERE role_name = ?", (role_name,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO roles (role_name, role_description) VALUES (?, ?)", (role_name, role_desc))

    # Ручне додавання правил
    rules_data = [
        ('duplicate_rule', 'Запис дублюється (оригінал дорівнює перекладу або вже був доданий)'),
        ('capitalization_rule', 'Перевірка першої великої літери'),
        ('double_quotes_rule', 'Заборонені подвійні лапки'),
        ('odd_quotes_rule', 'Непарна кількість одинарних лапок'),
        ('percent_rule', 'Перевірка відсотків у перекладі'),
        ('round_brackets_rule', 'Помилка з круглими дужками'),
        ('single_quotes_rule', 'Перевірка одинарних лапок'),
        ('tilde_rule', 'Перевірка тильди'),
        ('exception_rule', 'Виняткова ситуація під час обробки')
    ]
    for rule_name, rule_desc in rules_data:
        cursor.execute("SELECT COUNT(*) FROM rules WHERE rule_name = ?", (rule_name,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO rules (rule_name, rule_description) VALUES (?, ?)", (rule_name, rule_desc))

    # Ручне додавання типів помилок
    error_types_data = [
        ('Duplicate', 'Помилка дублювання'),
        ('Rule Violation', 'Порушення правил перевірки'),
        ('Exception', 'Виняткова ситуація')
    ]
    for et_name, et_desc in error_types_data:
        cursor.execute("SELECT COUNT(*) FROM error_types WHERE error_type_name = ?", (et_name,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO error_types (error_type_name, error_type_description) VALUES (?, ?)",
                           (et_name, et_desc))


def get_role_id(role_name, cursor):
    cursor.execute("SELECT role_id FROM roles WHERE role_name = ?", (role_name,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_rule_id(rule_name, cursor):
    cursor.execute("SELECT rule_id FROM rules WHERE rule_name = ?", (rule_name,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_error_type_id(error_type_name, cursor):
    cursor.execute("SELECT error_type_id FROM error_types WHERE error_type_name = ?", (error_type_name,))
    row = cursor.fetchone()
    return row[0] if row else None


def save_run_full(run_data, files_data, db_path='poChecker.db'):
    """
    Зберігає запуск перевірки, дані про файли та помилки.
    Повертає run_id, щоб його можна було використати для генерації файлу результатів.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO runs (run_date, directory, total_files, total_errors, user_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          run_data.get('directory'),
          run_data.get('total_files'),
          run_data.get('total_errors'),
          run_data.get('user_id')
          ))
    run_id = cursor.lastrowid

    for file_data in files_data:
        cursor.execute('''
            INSERT INTO files (run_id, file_name, file_path)
            VALUES (?, ?, ?)
        ''', (run_id, file_data.get('file_name'), file_data.get('file_path')))
        file_id = cursor.lastrowid

        for error in file_data.get('errors', []):
            rule_name = error.get('rule', 'exception_rule')
            if rule_name == 'duplicate_rule':
                error_type_name = 'Duplicate'
            elif rule_name == 'exception_rule':
                error_type_name = 'Exception'
            else:
                error_type_name = 'Rule Violation'
            rule_id = get_rule_id(rule_name, cursor)
            error_type_id = get_error_type_id(error_type_name, cursor)
            cursor.execute('''
                INSERT INTO errors (file_id, rule_id, error_type_id, line_number, error_description, original, translated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_id,
                rule_id,
                error_type_id,
                error.get('line_number', 0),
                error.get('error_description', ''),
                error.get('original', ''),
                error.get('translated', '')
            ))
    conn.commit()
    conn.close()
    return run_id


def generate_all_errors_file(files_data, run_id, results_folder='results'):
    """
    Генерує текстовий файл з деталізацією помилок для запуску run_id.
    Повертає шлях до згенерованого файлу.
    """
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    filename = f"all_errors_{run_id}.txt"
    filepath = os.path.join(results_folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for file_data in files_data:
            f.write("====================================\n")
            f.write(f"File: {file_data.get('file_name')}\n")
            f.write(f"Path: {file_data.get('file_path')}\n")
            for error in file_data.get('errors', []):
                f.write("====================================\n")
                f.write(f"Line: {error.get('line_number')}\n")
                f.write(f"Description: {error.get('error_description')}\n")
                f.write(f"Original: {error.get('original')}\n")
                f.write(f"Translated: {error.get('translated')}\n")
            f.write("====================================\n\n")
    return filepath
