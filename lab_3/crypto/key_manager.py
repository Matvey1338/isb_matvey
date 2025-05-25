import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from ..config.crypto_config import CryptoConfig, default_config

class KeyManager:
    def __init__(self, config: CryptoConfig = default_config):
        self.config = config

    def generate_symmetric_keys(self):
        private = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.config.ASYMMETRIC_KEY_SIZE
        )
        public = private.public_key()
        return private, public

    def generate_symmetric_key(self) -> bytes:
        return os.urandom(self.config.SYMMETRIC_KEY_SIZE // 8)

    def serialize_private(self, private_key, path: str = None):
        if path is None:
            path = self.config.PRIVATE_KEY_PATH
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(path, 'wb') as f:
            f.write(pem)

    def serialize_public(self, public_key, path: str = None):
        if path is None:
            path = self.config.PUBLIC_KEY_PATH
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(path, 'wb') as f:
            f.write(pem)

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