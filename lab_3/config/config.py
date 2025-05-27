import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

@dataclass
class Config:
    """
    Configuration class for application settings
    :param initial_file: path to initial file
    :param encrypted_file: path to encrypted file
    :param decrypted_file: path to decrypted file
    :param symmetric_key: path to symmetric key file
    :param public_key: path to public key file
    :param private_key: path to private key file
    :param key_size: size of symmetric key in bits
    :param rsa_key_size: size of RSA key in bits
    :param directories: list of directories to create
    """
    # File paths
    initial_file: str
    encrypted_file: str
    decrypted_file: str
    
    # Key paths
    symmetric_key: str
    public_key: str
    private_key: str
    
    # Crypto settings
    key_size: int
    rsa_key_size: int
    
    # Directories to create
    directories: List[str]

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """
        Get default configuration settings
        :return: dictionary with default configuration
        """
        return {
            "files": {
                "initial": "uploads/plain.txt",
                "encrypted": "uploads/encrypted.bin",
                "decrypted": "uploads/decrypted.txt"
            },
            "keys": {
                "symmetric": "keys/sym_key.enc",
                "public": "keys/public.pem",
                "private": "keys/private.pem"
            },
            "crypto": {
                "key_size": 128,
                "rsa_key_size": 2048
            },
            "directories": [
                "uploads",
                "keys"
            ]
        }

    @staticmethod
    def write_config_to_file(config_path: str, config_data: Dict[str, Any]) -> None:
        """
        Write configuration to JSON file
        :param config_path: path to configuration file
        :param config_data: configuration data to write
        :raises Exception: if writing fails
        """
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls, config_path: str = None) -> 'Config':
        """
        Load configuration from JSON file
        :param config_path: path to configuration file (optional)
        :return: Config instance
        :raises ValueError: if JSON format is invalid
        :raises KeyError: if required configuration key is missing
        :raises Exception: for other errors
        """
        if config_path is None:
            config_path = Path(__file__).parent / "settings.json"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Create instance
            config = cls(
                initial_file=config_data["files"]["initial"],
                encrypted_file=config_data["files"]["encrypted"],
                decrypted_file=config_data["files"]["decrypted"],
                symmetric_key=config_data["keys"]["symmetric"],
                public_key=config_data["keys"]["public"],
                private_key=config_data["keys"]["private"],
                key_size=config_data["crypto"]["key_size"],
                rsa_key_size=config_data["crypto"]["rsa_key_size"],
                directories=config_data["directories"]
            )
            
            # Ensure directories exist
            for directory in config.directories:
                os.makedirs(directory, exist_ok=True)
            
            return config
            
        except FileNotFoundError:
            # Create default config if file doesn't exist
            default_config = cls.get_default_config()
            cls.write_config_to_file(config_path, default_config)
            return cls.from_json(config_path)
            
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in configuration file {config_path}")
        except KeyError as e:
            raise KeyError(f"Missing required configuration key: {e}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")