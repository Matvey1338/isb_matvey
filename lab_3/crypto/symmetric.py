import os
from enum import Enum
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class EncryptionMode(Enum):
    """Режимы шифрования"""
    CBC = 'CBC'
    ECB = 'ECB'
    CFB = 'CFB'
    OFB = 'OFB'

class SymmetricCipher:
    """Class for Symmetric Cipher"""
    def __init__(self, key: bytes, mode: EncryptionMode = EncryptionMode.CBC, iv: bytes = None):
        if len(key) != 16:
            raise ValueError("IDEA requires a 16-byte key")
        self.key = key
        self.mode = mode
        
        # Выбор режима шифрования
        match self.mode:
            case EncryptionMode.CBC:
                self.iv = iv or os.urandom(8)
                mode_obj = modes.CBC(self.iv)
            case EncryptionMode.ECB:
                mode_obj = modes.ECB()
            case EncryptionMode.CFB:
                self.iv = iv or os.urandom(8)
                mode_obj = modes.CFB(self.iv)
            case EncryptionMode.OFB:
                self.iv = iv or os.urandom(8)
                mode_obj = modes.OFB(self.iv)
            case _:
                raise ValueError(f"Неподдерживаемый режим шифрования: {mode}")
            
        self.cipher = Cipher(
            algorithms.IDEA(self.key),
            mode_obj,
            backend=default_backend()
        )

    def encrypt(self, data: bytes) -> bytes:
        """IDEA Data Encryption"""
        try:
            padder = padding.PKCS7(64).padder()
            padded_data = padder.update(data) + padder.finalize()
            encryptor = self.cipher.encryptor()
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            
            # Добавляем IV только для режимов, которые его используют
            match self.mode:
                case EncryptionMode.CBC | EncryptionMode.CFB | EncryptionMode.OFB:
                    return self.iv + encrypted
                case EncryptionMode.ECB:
                    return encrypted
                case _:
                    raise ValueError(f"Неподдерживаемый режим шифрования: {self.mode}")
        except Exception as e:
            raise RuntimeError(f"Ошибка шифрования IDEA: {str(e)}")

    def decrypt(self, token: bytes) -> bytes:
        """IDEA Data Decryption"""
        try:
            # Извлекаем IV для режимов, которые его используют
            match self.mode:
                case EncryptionMode.CBC | EncryptionMode.CFB | EncryptionMode.OFB:
                    iv, ct = token[:8], token[8:]
                    cipher = Cipher(
                        algorithms.IDEA(self.key),
                        modes.CBC(iv) if self.mode == EncryptionMode.CBC else
                        modes.CFB(iv) if self.mode == EncryptionMode.CFB else
                        modes.OFB(iv),
                        backend=default_backend()
                    )
                case EncryptionMode.ECB:
                    ct = token
                    cipher = self.cipher
                case _:
                    raise ValueError(f"Неподдерживаемый режим шифрования: {self.mode}")
                
            decryptor = cipher.decryptor()
            padded = decryptor.update(ct) + decryptor.finalize()
            unpadder = padding.PKCS7(64).unpadder()
            return unpadder.update(padded) + unpadder.finalize()
        except Exception as e:
            raise RuntimeError(f"Ошибка дешифрования IDEA: {str(e)}")