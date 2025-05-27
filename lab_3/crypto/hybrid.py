import os
from .symmetric import SymmetricCipher, EncryptionMode
from .asymmetric import AsymmetricCipher
from crypto.key_manager import KeyManager
from crypto.key_file_manager import KeyFileManager
from config.config import Config

class HybridCipher:
    """Class for Hybrid Cipher"""
    def __init__(self, config: Config):
        """
        Initialize HybridCipher
        :param config: configuration object
        :return: None
        """
        self.key_manager = KeyManager(config)
        self.key_file_manager = KeyFileManager(config)
        self.config = config

    def encrypt_file(self, input_path: str, output_path: str, priv_path: str, enc_sym_path: str, mode: EncryptionMode = EncryptionMode.CBC) -> None:
        """
        Encrypts file using hybrid encryption
        :param input_path: path to input file
        :param output_path: path to save encrypted file
        :param priv_path: path to private key file
        :param enc_sym_path: path to encrypted symmetric key file
        :param mode: encryption mode (default: CBC)
        :return: None
        """
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

    def decrypt_file(self, input_path: str, output_path: str, priv_path: str, enc_sym_path: str, mode: EncryptionMode = EncryptionMode.CBC) -> None:
        """
        Decrypts file using hybrid decryption
        :param input_path: path to encrypted file
        :param output_path: path to save decrypted file
        :param priv_path: path to private key file
        :param enc_sym_path: path to encrypted symmetric key file
        :param mode: encryption mode (default: CBC)
        :return: None
        """
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