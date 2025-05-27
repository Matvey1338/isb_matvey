from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes

class AsymmetricCipher:
    """Class for Asymmetric Cipher"""
    @staticmethod
    def encrypt(public_key, data: bytes) -> bytes:
        """
        Encrypts data using asymmetric encryption
        :param public_key: public key for encryption
        :param data: data to encrypt
        :return: encrypted data
        """
        try:
            return public_key.encrypt(
                data,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(), label=None
                )
            )
        except Exception as e:
            raise RuntimeError(f"Ошибка асимметричного шифрования: {str(e)}")

    @staticmethod
    def decrypt(private_key, token: bytes) -> bytes:
        """
        Decrypts data using asymmetric decryption
        :param private_key: private key for decryption
        :param token: encrypted data to decrypt
        :return: decrypted data
        """
        try:
            return private_key.decrypt(
                token,
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(), label=None
                )
            )
        except Exception as e:
            raise RuntimeError(f"Ошибка асимметричного дешифрования: {str(e)}")