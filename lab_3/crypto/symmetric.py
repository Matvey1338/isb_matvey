import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class SymmetricCipher:
    """Class for Symmetric Cipher"""
    def __init__(self, key: bytes, iv: bytes = None):
        if len(key) != 16:
            raise ValueError("IDEA requires a 16-byte key")
        self.key = key
        self.iv = iv or os.urandom(8)
        self.cipher = Cipher(
            algorithms.IDEA(self.key),
            modes.CBC(self.iv),
            backend=default_backend()
        )

    def encrypt(self, data: bytes) -> bytes:
        """IDEA Data Encryption"""
        try:
            padder = padding.PKCS7(64).padder()
            padded_data = padder.update(data) + padder.finalize()
            encryptor = self.cipher.encryptor()
            return self.iv + encryptor.update(padded_data) + encryptor.finalize()
        except Exception as e:
            raise RuntimeError(f"Ошибка шифрования IDEA: {str(e)}")

    def decrypt(self, token: bytes) -> bytes:
        """IDEA Data Decryption"""
        try:
            iv, ct = token[:8], token[8:]
            cipher = Cipher(
                algorithms.IDEA(self.key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            padded = decryptor.update(ct) + decryptor.finalize()
            unpadder = padding.PKCS7(64).unpadder()
            return unpadder.update(padded) + unpadder.finalize()
        except Exception as e:
            raise RuntimeError(f"Ошибка дешифрования IDEA: {str(e)}")