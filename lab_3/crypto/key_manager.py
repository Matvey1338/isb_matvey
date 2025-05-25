import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from config.crypto_config import CryptoConfig, default_config
from crypto.asymmetric import AsymmetricCipher
from crypto.key_file_manager import KeyFileManager

class KeyManager:
    def __init__(self, config: CryptoConfig = default_config):
        self.config = config
        self.file_manager = KeyFileManager(config)

    def generate_all(self, sym_size: int, public_path: str, private_path: str, encrypted_sym_path: str) -> bytes:
        # generate symmetric key
        sym_key = self.generate_symmetric_key(sym_size)
        
        # generate RSA pair
        priv, pub = self.generate_asymmetric_keys()
        
        # serialize keys
        self.file_manager.serialize_private(priv, private_path)
        self.file_manager.serialize_public(pub, public_path)
        
        # encrypt symmetric key
        enc_sym = AsymmetricCipher.encrypt(pub, sym_key)
        self.file_manager.save_encrypted_symmetric_key(enc_sym, encrypted_sym_path)
        
        return sym_key

    def generate_asymmetric_keys(self):
        private = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.config.rsa_key_size
        )
        public = private.public_key()
        return private, public

    def generate_symmetric_key(self, size: int = None) -> bytes:
        if size is None:
            size = self.config.key_size
        return os.urandom(size // 8)
