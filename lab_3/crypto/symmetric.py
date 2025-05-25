import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

class SymmetricCipher:
    def __init__(self, key: bytes, iv: bytes = None):
        self.key = key
        self.iv = iv or os.urandom(16)
        self.cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))

    def encrypt(self, data: bytes) -> bytes:
        padder = padding.ANSIX923(128).padder()
        padded = padder.update(data) + padder.finalize()
        encryptor = self.cipher.encryptor()
        return self.iv + encryptor.update(padded) + encryptor.finalize()

    def decrypt(self, token: bytes) -> bytes:
        iv, ct = token[:16], token[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ct) + decryptor.finalize()
        unpadder = padding.ANSIX923(128).unpadder()
        return unpadder.update(padded) + unpadder.finalize()