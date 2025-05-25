from dataclasses import dataclass

@dataclass
class CryptoConfig:
    # Symmetric encryption parameters
    SYMMETRIC_KEY_SIZE: int = 256  # in bits
    
    # Asymmetric encryption parameters
    RSA_KEY_SIZE: int = 2048  # in bits
    
    # Hash parameters
    HASH_ALGORITHM: str = "SHA256"
    
    # Padding parameters
    PADDING_SCHEME: str = "PKCS7"
    
    # File paths
    PRIVATE_KEY_PATH: str = "private_key.pem"
    PUBLIC_KEY_PATH: str = "public_key.pem"

# Create a default configuration instance
default_config = CryptoConfig() 