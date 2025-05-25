import os
from cryptography.hazmat.primitives import serialization
from ..config.crypto_config import CryptoConfig, default_config

class KeyManager:
    def __init__(self, config: CryptoConfig = default_config):
        self.config = config

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
        if path is None:
            path = self.config.PRIVATE_KEY_PATH
        with open(path, 'rb') as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    def load_public(self, path: str = None):
        if path is None:
            path = self.config.PUBLIC_KEY_PATH
        with open(path, 'rb') as f:
            return serialization.load_pem_public_key(f.read()) 