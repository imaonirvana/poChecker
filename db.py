import sqlite3
from datetime import datetime

def init_db(db_path='poChecker.db'):
    """
    Ініціалізує базу даних. Якщо файл БД не існує, створює необхідні таблиці.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date TEXT,
            directory TEXT,
            total_files INTEGER,
            total_errors INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            file_name TEXT,
            line_number INTEGER,
            error_description TEXT,
            original TEXT,
            translated TEXT,
            FOREIGN KEY(run_id) REFERENCES runs(id)
        )
    ''')

    conn.commit()
    conn.close()

def save_run(run_data, errors, db_path='poChecker.db'):
    """
    Зберігає дані про запуск перевірки та всі знайдені помилки.

    Параметри:
      - run_data: словник з ключами 'directory', 'total_files', 'total_errors'
      - errors: список словників з даними про помилки
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO runs (run_date, directory, total_files, total_errors)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          run_data.get('directory'),
          run_data.get('total_files'),
          run_data.get('total_errors')))
    run_id = cursor.lastrowid

    for error in errors:
        cursor.execute('''
            INSERT INTO errors (run_id, file_name, line_number, error_description, original, translated)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            run_id,
            error.get('file_name'),
            error.get('line_number'),
            error.get('error_description'),
            error.get('original'),
            error.get('translated', '')
        ))

    conn.commit()
    conn.close()
