from cryptography.hazmat.primitives import serialization
from pathlib import Path
from config.crypto_config import CryptoConfig, default_config

class KeyFileManager:
    """
    Class for managing cryptographic key files
    :param config: configuration object for key file management
    """
    def __init__(self, config: CryptoConfig = default_config):
        self.config = config

    def _write_to_file(self, path: str, data: bytes) -> None:
        """
        Write binary data to file
        :param path: path to file
        :param data: binary data to write
        :raises Exception: if writing fails
        """
        try:
            with open(path, 'wb') as f:
                f.write(data)
        except Exception as e:
            raise Exception(f"Error writing to file {path}: {str(e)}")

    def _read_from_file(self, path: str) -> bytes:
        """
        Read binary data from file
        :param path: path to file
        :return: binary data read from file
        :raises FileNotFoundError: if file not found
        :raises Exception: if reading fails
        """
        try:
            with open(path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found at {path}")
        except Exception as e:
            raise Exception(f"Error reading from file {path}: {str(e)}")

    def serialize_private(self, private_key, path: str = None) -> None:
        """
        Serialize and save private key
        :param private_key: private key to serialize
        :param path: path to save key (optional)
        :raises Exception: if serialization or saving fails
        """
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
            self._write_to_file(path, pem)
        except Exception as e:
            raise Exception(f"Error serializing private key: {str(e)}")

    def serialize_public(self, public_key, path: str = None) -> None:
        """
        Serialize and save public key
        :param public_key: public key to serialize
        :param path: path to save key (optional)
        :raises Exception: if serialization or saving fails
        """
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
            self._write_to_file(path, pem)
        except Exception as e:
            raise Exception(f"Error serializing public key: {str(e)}")

    def load_private(self, path: str = None):
        """
        Load private key from file
        :param path: path to private key file (optional)
        :return: loaded private key
        :raises FileNotFoundError: if file not found
        :raises Exception: if loading fails
        """
        try:
            match path:
                case None:
                    path = self.config.PRIVATE_KEY_PATH
                case _:
                    pass
            data = self._read_from_file(path)
            return serialization.load_pem_private_key(data, password=None)
        except FileNotFoundError:
            raise FileNotFoundError(f"Private key file not found at {path}")
        except Exception as e:
            raise Exception(f"Error loading private key: {str(e)}")

    def load_public(self, path: str = None):
        """
        Load public key from file
        :param path: path to public key file (optional)
        :return: loaded public key
        :raises FileNotFoundError: if file not found
        :raises Exception: if loading fails
        """
        try:
            match path:
                case None:
                    path = self.config.PUBLIC_KEY_PATH
                case _:
                    pass
            data = self._read_from_file(path)
            return serialization.load_pem_public_key(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Public key file not found at {path}")
        except Exception as e:
            raise Exception(f"Error loading public key: {str(e)}")

    def save_encrypted_symmetric_key(self, encrypted_key: bytes, path: str) -> None:
        """
        Save encrypted symmetric key to file
        :param encrypted_key: encrypted key to save
        :param path: path to save key
        :raises Exception: if saving fails
        """
        try:
            self._write_to_file(path, encrypted_key)
        except Exception as e:
            raise Exception(f"Error saving encrypted symmetric key: {str(e)}") 