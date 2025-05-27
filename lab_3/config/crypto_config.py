import json
from dataclasses import dataclass
from pathlib import Path
from crypto.symmetric import EncryptionMode

@dataclass
class CryptoConfig:
    """
    Configuration class for cryptographic operations
    """
    def _read_config_file(self, config_path: str) -> dict:
        """
        Read and parse JSON configuration file
        :param config_path: path to configuration file
        :return: parsed configuration data
        :raises FileNotFoundError: if configuration file not found
        :raises ValueError: if JSON format is invalid
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in configuration file {config_path}")

    def __init__(self, config_path: str = None):
        """
        Initialize CryptoConfig with default or loaded configuration
        :param config_path: path to configuration file (optional)
        :raises FileNotFoundError: if configuration file not found
        :raises ValueError: if JSON format is invalid
        :raises KeyError: if required configuration key is missing
        :raises Exception: for other errors
        """
        if config_path is None:
            config_path = Path(__file__).parent / "crypto_config.json"
        
        try:
            config_data = self._read_config_file(config_path)
            
            # Initialize dataclass fields
            self.symmetric_key_size = config_data["symmetric"]["key_size"]
            self.encryption_mode = EncryptionMode[config_data["symmetric"]["mode"]]
            self.rsa_key_size = config_data["asymmetric"]["key_size"]
            self.hash_algorithm = config_data["hash"]["algorithm"]
            self.padding_scheme = config_data["padding"]["scheme"]
            self.private_key_path = config_data["paths"]["private_key"]
            self.public_key_path = config_data["paths"]["public_key"]
            
        except KeyError as e:
            raise KeyError(f"Missing required configuration key: {e}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}") 