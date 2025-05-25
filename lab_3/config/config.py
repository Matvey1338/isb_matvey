import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class Config:
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

    @classmethod
    def from_json(cls, config_path: str = None):
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
            default_config = {
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
                    "key_size": 256,
                    "rsa_key_size": 4096
                },
                "directories": [
                    "uploads",
                    "keys"
                ]
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=4)
            
            return cls.from_json(config_path)
            
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in configuration file {config_path}")
        except KeyError as e:
            raise KeyError(f"Missing required configuration key: {e}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")

# Create a default configuration instance
default_config = Config.from_json()