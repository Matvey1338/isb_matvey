import os
from flask import Flask, render_template, request, session, url_for, redirect, flash
from cipher.vigenere import VigenereCipher
from cipher.utils import save_key
import secrets

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

    timestamp = secrets.token_hex(4)
    key_file = os.path.join(OUTPUT_DIR, f'key_{timestamp}.json')

    save_key(key, {
        'original_text': text,
        'encrypted_text': encrypted_text
    }, key_file)

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

    timestamp = secrets.token_hex(4)
    key_file = os.path.join(OUTPUT_DIR, f'key_{timestamp}.json')

    save_key(key, {
        'timestamp': timestamp,
        'original_text': text,
        'encrypted_text': decrypted_text
    }, key_file)

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
