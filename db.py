import sqlite3
import os
from datetime import datetime


def init_db(db_path='poChecker.db'):
    """
    Створює (за потреби) всі таблиці та викликає заповнення статичних даних.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Таблиця runs (інформація про запуск)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date TEXT,
            directory TEXT,
            total_files INTEGER,
            total_errors INTEGER
        )
    ''')

    # 2. Таблиця files (список файлів, оброблених у межах одного запуску)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            file_name TEXT,
            file_path TEXT,
            FOREIGN KEY(run_id) REFERENCES runs(run_id)
        )
    ''')

    # 3. Таблиця rules (усі можливі правила)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT UNIQUE,
            rule_description TEXT
        )
    ''')

    # 4. Таблиця error_types (типи помилок)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_types (
            error_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_type_name TEXT,
            error_type_description TEXT
        )
    ''')

    # 5. Таблиця errors (кожна помилка, з посиланням на файл, правило і тип помилки)
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
    # Заповнюємо таблиці rules та error_types статичними даними
    populate_static_data(cursor)
    conn.commit()
    conn.close()


def populate_static_data(cursor):
    """
    Ручне заповнення таблиці rules усіма правилами, які є в проєкті,
    а також таблиці error_types.
    """
    # === Ручне додавання правил (додайте свої за потреби) ===
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
        # Додавайте інші правила за потреби
    ]
    for rule_name, rule_desc in rules_data:
        cursor.execute("SELECT COUNT(*) FROM rules WHERE rule_name = ?", (rule_name,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO rules (rule_name, rule_description)
                VALUES (?, ?)
            """, (rule_name, rule_desc))

    # === Типи помилок ===
    # Ви можете розширити список типів (якщо хочете деталізувати помилки).
    error_types_data = [
        ('Duplicate', 'Помилка дублювання'),
        ('Rule Violation', 'Порушення правил перевірки'),
        ('Exception', 'Виняткова ситуація')
    ]
    for et_name, et_desc in error_types_data:
        cursor.execute("SELECT COUNT(*) FROM error_types WHERE error_type_name = ?", (et_name,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO error_types (error_type_name, error_type_description)
                VALUES (?, ?)
            """, (et_name, et_desc))


def get_rule_id(rule_name, cursor):
    """
    Повертає rule_id за rule_name.
    """
    cursor.execute("SELECT rule_id FROM rules WHERE rule_name = ?", (rule_name,))
    row = cursor.fetchone()
    return row[0] if row else None


def get_error_type_id(error_type_name, cursor):
    """
    Повертає error_type_id за error_type_name.
    """
    cursor.execute("SELECT error_type_id FROM error_types WHERE error_type_name = ?", (error_type_name,))
    row = cursor.fetchone()
    return row[0] if row else None


def save_run_full(run_data, files_data, db_path='poChecker.db'):
    """
    Зберігає запуск перевірки, дані про файли та помилки.

    run_data: словник з ключами 'directory', 'total_files', 'total_errors'
    files_data: список словників, кожен з яких описує файл:
       {
         'file_name': ...,
         'file_path': ...,
         'errors': [
             {
               'line_number': ...,
               'error_description': ...,
               'original': ...,
               'translated': ...,
               'rule': 'capitalization_rule' / 'duplicate_rule' / ... / 'exception_rule'
             },
             ...
         ]
       }
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Запис про запуск
    cursor.execute('''
        INSERT INTO runs (run_date, directory, total_files, total_errors)
        VALUES (?, ?, ?, ?)
    ''', (
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        run_data.get('directory'),
        run_data.get('total_files'),
        run_data.get('total_errors')
    ))
    run_id = cursor.lastrowid

    # 2. Для кожного файлу записуємо інформацію у таблицю files
    for file_data in files_data:
        cursor.execute('''
            INSERT INTO files (run_id, file_name, file_path)
            VALUES (?, ?, ?)
        ''', (run_id, file_data.get('file_name'), file_data.get('file_path')))
        file_id = cursor.lastrowid

        # 3. Для кожної помилки в цьому файлі робимо запис у таблицю errors
        for error in file_data.get('errors', []):
            rule_name = error.get('rule', 'exception_rule')  # Якщо не вказано, то припустимо Exception
            # Мапимо rule_name -> error_type
            # Наприклад, якщо rule_name == 'duplicate_rule', то error_type = 'Duplicate'
            # Якщо rule_name == 'exception_rule', то error_type = 'Exception'
            # Інакше -> 'Rule Violation'
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
