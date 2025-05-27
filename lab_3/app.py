from flask import Flask, request, render_template, redirect, url_for, flash
import os
from pathlib import Path
from config.config import Config, default_config
from crypto.hybrid import HybridCipher
from crypto.key_manager import KeyManager
from crypto.key_file_manager import KeyFileManager

class CryptoApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(16)
        self.config = default_config
        self.key_manager = KeyManager(self.config)
        self.key_file_manager = KeyFileManager(self.config)
        self.hybrid_cipher = HybridCipher(self.config)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/generate', methods=['GET', 'POST'])
        def generate_view():
            if request.method == 'POST':
                try:
                    paths = {
                        'public_key': request.form['public_key_path'],
                        'private_key': request.form['private_key_path'],
                        'sym_key': request.form['sym_key_path']
                    }
                    
                    # Generate all keys
                    sym_key = self.key_manager.generate_all(
                        paths['public_key'],
                        paths['private_key'],
                        paths['sym_key']
                    )
                    
                    flash('Ключи успешно сгенерированы')
                    return redirect(url_for('index'))
                except Exception as e:
                    flash(f'Ошибка при генерации ключей: {str(e)}')
                    return redirect(url_for('generate_view'))
            return render_template('generate.html')

        @self.app.route('/encrypt', methods=['GET', 'POST'])
        def encrypt_view():
            if request.method == 'POST':
                try:
                    input_type = request.form.get('input_type', 'file')
                    out = os.path.join('uploads', request.form['output_name'])
                    priv = request.form['private_key_path']
                    symk = request.form['sym_key_path']

                    match input_type:
                        case 'file':
                            f = request.files['file']
                            input_path = os.path.join('uploads', f.filename)
                            f.save(input_path)
                            self.hybrid_cipher.encrypt_file(input_path, out, priv, symk)
                        case _:  # text input
                            text = request.form['text']
                            input_path = os.path.join('uploads', 'temp_input.txt')
                            with open(input_path, 'w', encoding='utf-8') as f:
                                f.write(text)
                            self.hybrid_cipher.encrypt_file(input_path, out, priv, symk)
                            os.remove(input_path)  # Clean up temporary file

                    flash('Файл зашифрован')
                    return redirect(url_for('index'))
                except Exception as e:
                    flash(f'Ошибка при шифровании: {str(e)}')
                    return redirect(url_for('encrypt_view'))
            return render_template('encrypt.html')

        @self.app.route('/decrypt', methods=['GET', 'POST'])
        def decrypt_view():
            if request.method == 'POST':
                try:
                    input_type = request.form.get('input_type', 'file')
                    out = os.path.join('uploads', request.form['output_name'])
                    priv = request.form['private_key_path']
                    symk = request.form['sym_key_path']

                    match input_type:
                        case 'file':
                            f = request.files['file']
                            input_path = os.path.join('uploads', f.filename)
                            f.save(input_path)
                            self.hybrid_cipher.decrypt_file(input_path, out, priv, symk)
                        case _:  # text input
                            text = request.form['text']
                            input_path = os.path.join('uploads', 'temp_input.txt')
                            with open(input_path, 'w', encoding='utf-8') as f:
                                f.write(text)
                            self.hybrid_cipher.decrypt_file(input_path, out, priv, symk)
                            os.remove(input_path)  # Clean up temporary file

                    flash('Файл расшифрован')
                    return redirect(url_for('index'))
                except Exception as e:
                    flash(f'Ошибка при расшифровании: {str(e)}')
                    return redirect(url_for('decrypt_view'))
            return render_template('decrypt.html')

    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == '__main__':
    app = CryptoApp()
    app.run(debug=True)