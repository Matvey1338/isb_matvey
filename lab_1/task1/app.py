import os
import secrets

from flask import (
    Flask,
    render_template,
    request,
    session,
    url_for,
    redirect,
    flash
)

from cipher.vigenere import VigenereCipher
from cipher.utils import save_key, get_next_index, save_file


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok = True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt', methods = ['POST'])
def encrypt():
    text = request.form.get('text', '')
    key = request.form.get('key', '')

    if not text:
        flash('Пожалуйста, введите текст для шифрования')
        return redirect(url_for('index'))

    if not key:
        flash('Пожалуйста, введите ключ шифрования')
        return redirect(url_for('index'))

    cipher = VigenereCipher(key)

    encrypted_text = cipher.encrypt(text)

    indexfile = get_next_index(OUTPUT_DIR)
    key_file = os.path.join(OUTPUT_DIR, f'key_{indexfile}.json')
    original_file = os.path.join(OUTPUT_DIR, f'original_{indexfile}.txt')
    encrypted_file = os.path.join(OUTPUT_DIR, f'encrypted_{indexfile}.txt')

    # Сохраняем ключ и информацию в JSON
    try:
        save_key(key, key_file)
    except Exception as e:
        print(f"Ошибка при сохранении ключа: {e}")

    # Сохраняем исходный текст
    try:
        save_file(original_file, text)
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")

    # Сохраняем зашифрованный текст
    try:
        save_file(encrypted_file, encrypted_text)
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")

    session['result'] = {
        'operation': 'encrypt',
        'original_text': text[:500] + ('...' if len(text) > 500 else ''),
        'processed_text': encrypted_text[:500] + ('...' if len(encrypted_text) > 500 else ''),
        'key': key,
        'key_file': key_file
    }

    return redirect(url_for('result'))


@app.route('/decrypt', methods = ['POST'])
def decrypt():
    text = request.form.get('text', '')
    key = request.form.get('key', '')

    if not text:
        flash('Пожалуйста, введите текст для дешифрования')
        return redirect(url_for('index'))

    if not key:
        flash('Пожалуйста, введите ключ шифрования')
        return redirect(url_for('index'))

    cipher = VigenereCipher(key)

    decrypted_text = cipher.decrypt(text)

    indexfile = get_next_index(OUTPUT_DIR)
    key_file = os.path.join(OUTPUT_DIR, f'key_{indexfile}.json')
    original_file = os.path.join(OUTPUT_DIR, f'original_encrypted_{indexfile}.txt')
    decrypted_file = os.path.join(OUTPUT_DIR, f'decrypted_{indexfile}.txt')

    try:
        save_key(key, key_file)
    except Exception as e:
        print(f"Ошибка при сохранении ключа: {e}")

    # Сохраняем исходный текст
    try:
        save_file(original_file, text)
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")

    # Сохраняем зашифрованный текст
    try:
        save_file(decrypted_file, decrypted_text)
    except Exception as e:
        print(f"Ошибка при сохранении в файл: {e}")


    session['result'] = {
        'operation': 'decrypt',
        'original_text': text[:500] + ('...' if len(text) > 500 else ''),
        'processed_text': decrypted_text[:500] + ('...' if len(decrypted_text) > 500 else ''),
        'key': key,
        'original_file': text,
        'processed_file': key,
        'key_file': key_file
    }

    return redirect(url_for('result'))


@app.route('/result')
def result():
    if 'result' not in session:
        return redirect(url_for('index'))

    return render_template('result.html', result = session['result'])


if __name__ == '__main__':
    app.run(debug = True)
