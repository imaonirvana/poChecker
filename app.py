from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from db import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замініть на надійний секретний ключ

DATABASE = 'poChecker.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'po'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Константа секретної фрази для модератора
MOD_SECRET = "mod_secret"


@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('upload'))
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):
        return redirect(url_for('upload'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        secret_phrase = request.form.get('secret_phrase', '').strip()
        # Якщо секретна фраза співпадає, роль – moderator, інакше – user
        role_name = "moderator" if secret_phrase == MOD_SECRET else "user"
        hashed_password = generate_password_hash(password)
        try:
            conn = get_db_connection()
            role_row = conn.execute("SELECT role_id FROM roles WHERE role_name = ?", (role_name,)).fetchone()
            role_id = role_row['role_id'] if role_row else None
            conn.execute('INSERT INTO users (username, password, role_id) VALUES (?, ?, ?)',
                         (username, hashed_password, role_id))
            conn.commit()
            flash('Реєстрація успішна! Тепер увійдіть в систему.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Користувач з таким логіном вже існує!', 'danger')
            return redirect(url_for('register'))
        except Exception as e:
            flash(f"Помилка: {str(e)}", 'danger')
            return redirect(url_for('register'))
        finally:
            conn.close()
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('upload'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_db_connection()
            user = conn.execute('''
                SELECT u.*, r.role_name 
                FROM users u
                LEFT JOIN roles r ON u.role_id = r.role_id
                WHERE u.username = ?
            ''', (username,)).fetchone()
            conn.close()
            if user and check_password_hash(user['password'], password):
                session['logged_in'] = True
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                session['role'] = user['role_name']
                flash('Вхід успішний!', 'success')
                return redirect(url_for('upload'))
            else:
                flash('Невірний логін або пароль', 'danger')
        except Exception as e:
            flash(f"Помилка: {str(e)}", 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'folder' not in request.files:
            flash('Не вибрано файлів', 'warning')
            return redirect(request.url)
        files = request.files.getlist('folder')
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Файли успішно завантажено, починається обробка...', 'info')

        # Автоматичний запуск обробки файлів
        from file_processor import process_po_files
        total_files, total_errors, files_data = process_po_files(app.config['UPLOAD_FOLDER'])

        # Зберігаємо результати запуску у базу даних
        from db import save_run_full, generate_all_errors_file, get_db_connection
        run_data = {
            'directory': app.config['UPLOAD_FOLDER'],
            'total_files': total_files,
            'total_errors': total_errors,
            'user_id': session.get('user_id')
        }
        run_id = save_run_full(run_data, files_data)

        # Генеруємо унікальний файл all_errors.txt для цього запуску
        result_filepath = generate_all_errors_file(files_data, run_id)

        # Оновлюємо запис у таблиці runs, додаючи шлях до файлу результатів
        conn = get_db_connection()
        conn.execute("UPDATE runs SET result_file = ? WHERE run_id = ?", (result_filepath, run_id))
        conn.commit()
        conn.close()

        # Створюємо окрему папку для змінених файлів для цього запуску
        import shutil
        modified_run_folder = os.path.join(os.getcwd(), 'modified', f'run_{run_id}')
        if not os.path.exists(modified_run_folder):
            os.makedirs(modified_run_folder)
        # Приклад копіювання (тут можна додати логіку для збереження модифікованого вмісту)
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.endswith('.po'):
                src = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                dst = os.path.join(modified_run_folder, "modified_" + filename)
                shutil.copy(src, dst)

        flash('Обробка завершена. Результати збережено.', 'success')
        return redirect(url_for('results'))

    return render_template('upload.html')


@app.route('/modified')
def modified_files():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    import os
    modified_folder = os.path.join(os.getcwd(), 'modified')
    if not os.path.exists(modified_folder):
        flash('Немає змінених файлів.', 'warning')
        return redirect(url_for('upload'))
    files = os.listdir(modified_folder)
    return render_template('modified.html', files=files)

@app.route('/modified/<int:run_id>')
def show_modified_files(run_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    import os
    modified_run_folder = os.path.join(os.getcwd(), 'modified', f'run_{run_id}')
    if not os.path.exists(modified_run_folder):
        flash('Немає змінених файлів для цього запуску.', 'warning')
        return redirect(url_for('upload'))
    files = os.listdir(modified_run_folder)
    return render_template('modified.html', files=files, run_id=run_id)


@app.route('/download_modified/<int:run_id>/<path:filename>')
def download_modified_run(run_id, filename):
    from flask import send_from_directory
    modified_run_folder = os.path.join(os.getcwd(), 'modified', f'run_{run_id}')
    return send_from_directory(directory=modified_run_folder, path=filename, as_attachment=True)


@app.route('/download_modified/<path:filename>')
def download_modified(filename):
    from flask import send_from_directory
    modified_folder = os.path.join(os.getcwd(), 'modified')
    return send_from_directory(directory=modified_folder, path=filename, as_attachment=True)

@app.route('/download/<path:filename>')
def download_result(filename):
    results_folder = os.path.join(os.getcwd(), 'results')
    return send_from_directory(results_folder, os.path.basename(filename), as_attachment=True)


@app.route('/results')
def results():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    role = session.get('role')
    user_id = session.get('user_id')
    if role == 'moderator':
        runs = conn.execute('SELECT * FROM runs ORDER BY run_date DESC').fetchall()
    else:
        runs = conn.execute('SELECT * FROM runs WHERE user_id = ? ORDER BY run_date DESC', (user_id,)).fetchall()

    # Для кожного запуску отримуємо підсумок помилок за типом
    run_details = {}
    for run in runs:
        details = conn.execute('''
            SELECT et.error_type_name, COUNT(*) as count
            FROM errors e
            JOIN files f ON e.file_id = f.file_id
            JOIN error_types et ON e.error_type_id = et.error_type_id
            WHERE f.run_id = ?
            GROUP BY et.error_type_name
        ''', (run['run_id'],)).fetchall()
        # Зберігаємо для конкретного run_id
        run_details[run['run_id']] = details
    conn.close()
    return render_template('results.html', runs=runs, run_details=run_details)



# Обробка помилок 404 та 500
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    from db import init_db
    init_db()  # Ініціалізуємо базу даних перед запуском сервера
    app.run(debug=True)

