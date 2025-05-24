import os
from .symmetric import SymmetricCipher
from .asymmetric import AsymmetricCipher

class HybridCipher:
    @staticmethod
    def generate_all(sym_size, public_path, private_path, encrypted_sym_path):
        # generate symmetric key
        sym_key = SymmetricCipher.generate_key(sym_size)
        # generate RSA pair
        priv, pub = AsymmetricCipher.generate_keys()
        # serialize keys
        AsymmetricCipher.serialize_private(priv, private_path)
        AsymmetricCipher.serialize_public(pub, public_path)
        # encrypt symmetric key
        enc_sym = AsymmetricCipher.encrypt_with_public(pub, sym_key)
        with open(encrypted_sym_path, 'wb') as f:
            f.write(enc_sym)
        return sym_key

    @staticmethod
    def encrypt_file(input_path, output_path, priv_path, enc_sym_path):
        priv = AsymmetricCipher.load_private(priv_path)
        with open(enc_sym_path, 'rb') as f:
            sym_key = AsymmetricCipher.decrypt_with_private(priv, f.read())
        cipher = SymmetricCipher(sym_key)
        with open(input_path, 'rb') as fin:
            data = fin.read()
        ct = cipher.encrypt(data)
        with open(output_path, 'wb') as fout:
            fout.write(ct)

    @staticmethod
    def decrypt_file(input_path, output_path, priv_path, enc_sym_path):
        priv = AsymmetricCipher.load_private(priv_path)
        with open(enc_sym_path, 'rb') as f:
            sym_key = AsymmetricCipher.decrypt_with_private(priv, f.read())
        cipher = SymmetricCipher(sym_key)
        with open(input_path, 'rb') as fin:
            data = fin.read()
        pt = cipher.decrypt(data)
        with open(output_path, 'wb') as fout:
            fout.write(pt)