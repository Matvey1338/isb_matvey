from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import os
from lab_3.config.config import Config
from crypto.hybrid import HybridCipher

# Инициализация
app = Flask(__name__)
app.secret_key = os.urandom(16)
config = Config()

# Роуты UI
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET','POST'])
def generate_view():
    if request.method == 'POST':
        size = int(request.form['key_size'])
        paths = {
            'public_key': request.form['public_key_path'],
            'private_key': request.form['private_key_path'],
            'sym_key': request.form['sym_key_path']
        }
        HybridCipher.generate_all(size, paths['public_key'],
                                  paths['private_key'], paths['sym_key'])
        flash('Ключи успешно сгенерированы')
        return redirect(url_for('index'))
    return render_template('generate.html')

@app.route('/encrypt', methods=['GET','POST'])
def encrypt_view():
    if request.method == 'POST':
        input_type = request.form.get('input_type', 'file')
        out = os.path.join('uploads', request.form['output_name'])
        priv = request.form['private_key_path']
        symk = request.form['sym_key_path']

        if input_type == 'file':
            f = request.files['file']
            input_path = os.path.join('uploads', f.filename)
            f.save(input_path)
            HybridCipher.encrypt_file(input_path, out, priv, symk)
        else:  # text input
            text = request.form['text']
            input_path = os.path.join('uploads', 'temp_input.txt')
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write(text)
            HybridCipher.encrypt_file(input_path, out, priv, symk)
            os.remove(input_path)  # Clean up temporary file

        flash('Файл зашифрован')
        return redirect(url_for('index'))
    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET','POST'])
def decrypt_view():
    if request.method == 'POST':
        input_type = request.form.get('input_type', 'file')
        out = os.path.join('uploads', request.form['output_name'])
        priv = request.form['private_key_path']
        symk = request.form['sym_key_path']

        if input_type == 'file':
            f = request.files['file']
            input_path = os.path.join('uploads', f.filename)
            f.save(input_path)
            HybridCipher.decrypt_file(input_path, out, priv, symk)
        else:  # text input
            text = request.form['text']
            input_path = os.path.join('uploads', 'temp_input.txt')
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write(text)
            HybridCipher.decrypt_file(input_path, out, priv, symk)
            os.remove(input_path)  # Clean up temporary file

        flash('Файл расшифрован')
        return redirect(url_for('index'))
    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(debug=True)