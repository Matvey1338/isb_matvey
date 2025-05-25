import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CryptoConfig:
    # Symmetric encryption parameters
    SYMMETRIC_KEY_SIZE: int
    # Asymmetric encryption parameters
    RSA_KEY_SIZE: int
    # Hash parameters
    HASH_ALGORITHM: str
    # Padding parameters
    PADDING_SCHEME: str
    # File paths
    PRIVATE_KEY_PATH: str
    PUBLIC_KEY_PATH: str

    @classmethod
    def from_json(cls, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent / "crypto_config.json"
        
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            return cls(
                SYMMETRIC_KEY_SIZE=config_data["symmetric"]["key_size"],
                RSA_KEY_SIZE=config_data["asymmetric"]["key_size"],
                HASH_ALGORITHM=config_data["hash"]["algorithm"],
                PADDING_SCHEME=config_data["padding"]["scheme"],
                PRIVATE_KEY_PATH=config_data["paths"]["private_key"],
                PUBLIC_KEY_PATH=config_data["paths"]["public_key"]
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in configuration file {config_path}")
        except KeyError as e:
            raise KeyError(f"Missing required configuration key: {e}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")

# Create a default configuration instance
default_config = CryptoConfig.from_json() 