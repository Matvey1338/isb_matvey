import os
from .symmetric import SymmetricCipher, EncryptionMode
from .asymmetric import AsymmetricCipher
from crypto.key_manager import KeyManager
from crypto.key_file_manager import KeyFileManager
from config.config import default_config

class HybridCipher:
    """Class for Hybrid Cipher"""
    def __init__(self, config=default_config):
        self.key_manager = KeyManager(config)
        self.key_file_manager = KeyFileManager(config)
        self.config = config

    def encrypt_file(self, input_path, output_path, priv_path, enc_sym_path, mode: EncryptionMode = EncryptionMode.CBC):
        """Encrypt file"""
        try:
            priv = self.key_file_manager.load_private(priv_path)
            with open(enc_sym_path, 'rb') as f:
                sym_key = AsymmetricCipher.decrypt(priv, f.read())
            cipher = SymmetricCipher(sym_key, mode=mode)
            with open(input_path, 'rb') as fin:
                data = fin.read()
            ct = cipher.encrypt(data)
            with open(output_path, 'wb') as fout:
                fout.write(ct)
        except FileNotFoundError as e:
            raise RuntimeError(f"Ошибка: файл не найден - {str(e)}")
        except PermissionError as e:
            raise RuntimeError(f"Ошибка доступа к файлу - {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Ошибка при шифровании файла: {str(e)}")

    def decrypt_file(self, input_path, output_path, priv_path, enc_sym_path, mode: EncryptionMode = EncryptionMode.CBC):
        """Decrypt file"""
        try:
            priv = self.key_file_manager.load_private(priv_path)
            with open(enc_sym_path, 'rb') as f:
                sym_key = AsymmetricCipher.decrypt(priv, f.read())
            cipher = SymmetricCipher(sym_key, mode=mode)
            with open(input_path, 'rb') as fin:
                data = fin.read()
            pt = cipher.decrypt(data)
            with open(output_path, 'wb') as fout:
                fout.write(pt)
        except FileNotFoundError as e:
            raise RuntimeError(f"Ошибка: файл не найден - {str(e)}")
        except PermissionError as e:
            raise RuntimeError(f"Ошибка доступа к файлу - {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Ошибка при дешифровании файла: {str(e)}")