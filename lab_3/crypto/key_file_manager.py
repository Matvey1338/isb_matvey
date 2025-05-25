from cryptography.hazmat.primitives import serialization
from pathlib import Path
from config.crypto_config import CryptoConfig, default_config

class KeyFileManager:
    def __init__(self, config: CryptoConfig = default_config):
        self.config = config

    def serialize_private(self, private_key, path: str = None):
        try:
            match path:
                case None:
                    path = self.config.PRIVATE_KEY_PATH
                case _:
                    pass
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(path, 'wb') as f:
                f.write(pem)
        except Exception as e:
            raise Exception(f"Error serializing private key: {str(e)}")

    def serialize_public(self, public_key, path: str = None):
        try:
            match path:
                case None:
                    path = self.config.PUBLIC_KEY_PATH
                case _:
                    pass
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            with open(path, 'wb') as f:
                f.write(pem)
        except Exception as e:
            raise Exception(f"Error serializing public key: {str(e)}")

    def load_private(self, path: str = None):
        try:
            match path:
                case None:
                    path = self.config.PRIVATE_KEY_PATH
                case _:
                    pass
            with open(path, 'rb') as f:
                return serialization.load_pem_private_key(f.read(), password=None)
        except FileNotFoundError:
            raise FileNotFoundError(f"Private key file not found at {path}")
        except Exception as e:
            raise Exception(f"Error loading private key: {str(e)}")

    def load_public(self, path: str = None):
        try:
            match path:
                case None:
                    path = self.config.PUBLIC_KEY_PATH
                case _:
                    pass
            with open(path, 'rb') as f:
                return serialization.load_pem_public_key(f.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"Public key file not found at {path}")
        except Exception as e:
            raise Exception(f"Error loading public key: {str(e)}")

    def save_encrypted_symmetric_key(self, encrypted_key: bytes, path: str):
        try:
            with open(path, 'wb') as f:
                f.write(encrypted_key)
        except Exception as e:
            raise Exception(f"Error saving encrypted symmetric key: {str(e)}") 