import json


class Config:
    def __init__(self, path="settings.json"):
        with open(path, 'r') as f:
            data = json.load(f)
        self.initial_file = data.get('initial_file')
        self.encrypted_file = data.get('encrypted_file')
        self.decrypted_file = data.get('decrypted_file')
        self.symmetric_key = data.get('symmetric_key')
        self.public_key = data.get('public_key')
        self.secret_key = data.get('secret_key')
        self.key_size = data.get('key_size', 256)