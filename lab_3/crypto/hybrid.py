import os
from .symmetric import SymmetricCipher
from .asymmetric import AsymmetricCipher
from crypto.key_manager import KeyManager
from crypto.key_file_manager import KeyFileManager
from config.config import default_config

class HybridCipher:
    def __init__(self, config=default_config):
        self.key_manager = KeyManager(config)
        self.key_file_manager = KeyFileManager(config)

    def encrypt_file(self, input_path, output_path, priv_path, enc_sym_path):
        priv = self.key_file_manager.load_private(priv_path)
        with open(enc_sym_path, 'rb') as f:
            sym_key = AsymmetricCipher.decrypt(priv, f.read())
        cipher = SymmetricCipher(sym_key)
        with open(input_path, 'rb') as fin:
            data = fin.read()
        ct = cipher.encrypt(data)
        with open(output_path, 'wb') as fout:
            fout.write(ct)

    def decrypt_file(self, input_path, output_path, priv_path, enc_sym_path):
        priv = self.key_file_manager.load_private(priv_path)
        with open(enc_sym_path, 'rb') as f:
            sym_key = AsymmetricCipher.decrypt(priv, f.read())
        cipher = SymmetricCipher(sym_key)
        with open(input_path, 'rb') as fin:
            data = fin.read()
        pt = cipher.decrypt(data)
        with open(output_path, 'wb') as fout:
            fout.write(pt)