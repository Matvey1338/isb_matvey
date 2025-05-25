from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes

class AsymmetricCipher:
    @staticmethod
    def generate_keys():
        private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public = private.public_key()
        return private, public

    @staticmethod
    def encrypt(public_key, data: bytes) -> bytes:
        return public_key.encrypt(
            data,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(), label=None
            )
        )

    @staticmethod
    def decrypt(private_key, token: bytes) -> bytes:
        return private_key.decrypt(
            token,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(), label=None
            )
        )