import json
import os

class Config:
    def __init__(self, path="settings.json"):
        # Если файл настроек отсутствует, создаём со значениями по умолчанию
        defaults = {
            'initial_file':'uploads/plain.txt',
            'encrypted_file':'uploads/encrypted.bin',
            'decrypted_file':'uploads/decrypted.txt',
            'symmetric_key':'keys/sym_key.enc',
            'public_key':'keys/public.pem',
            'secret_key':'keys/private.pem',
            'key_size':256
        }
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(defaults, f, ensure_ascii=False, indent=4)
        # Загружаем настройки
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Пути
        self.initial_file = data.get('initial_file')
        self.encrypted_file = data.get('encrypted_file')
        self.decrypted_file = data.get('decrypted_file')
        self.symmetric_key = data.get('symmetric_key')
        self.public_key = data.get('public_key')
        self.secret_key = data.get('secret_key')
        self.key_size = data.get('key_size', 256)
        # Ensure directories exist
        for d in ['logs', 'uploads', 'keys']:
            os.makedirs(d, exist_ok=True)