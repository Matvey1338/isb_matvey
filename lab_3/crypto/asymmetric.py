from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes

class AsymmetricCipher:
    @staticmethod
    def generate_keys():
        private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public = private.public_key()
        return private, public

    @staticmethod
    def serialize_private(private_key, path: str):
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(path, 'wb') as f:
            f.write(pem)

    @staticmethod
    def serialize_public(public_key, path: str):
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(path, 'wb') as f:
            f.write(pem)

    @staticmethod
    def load_private(path: str):
        with open(path, 'rb') as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    @staticmethod
    def load_public(path: str):
        with open(path, 'rb') as f:
            return serialization.load_pem_public_key(f.read())

    def encrypt_with_public(public_key, data: bytes) -> bytes:
        return public_key.encrypt(
            data,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(), label=None
            )
        )

    def decrypt_with_private(private_key, token: bytes) -> bytes:
        return private_key.decrypt(
            token,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(), label=None
            )
        )