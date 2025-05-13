from .config import SEQUENCE_LENGTH, BLOCK_SIZE

def validate_sequence_length(sequence):
    """
    Validates if sequence has correct length according to SEQUENCE_LENGTH constant
    
    Args:
        sequence (list or str): Sequence of bits to validate
        
    Returns:
        dict: Dictionary containing validation result
            {
                'is_valid' (bool): True if sequence length is correct, False otherwise
                'error' (str, optional): Error message if validation failed
            }
    """
    n = len(sequence)
    if n != SEQUENCE_LENGTH:
        return {
            'is_valid': False,
            'error': f'Sequence length should be {SEQUENCE_LENGTH} bits'
        }
    return {'is_valid': True}

def validate_block_size(sequence, block_size=BLOCK_SIZE):
    """
    Validates if sequence can be divided into blocks of specified size
    
    Args:
        sequence (list or str): Sequence of bits to validate
        block_size (int, optional): Size of each block. Defaults to BLOCK_SIZE constant
        
    Returns:
        dict: Dictionary containing validation result
            {
                'is_valid' (bool): True if sequence can be divided into blocks, False otherwise
                'error' (str, optional): Error message if validation failed
            }
    """
    n = len(sequence)
    N = n // block_size
    if N < 1:
        return {
            'is_valid': False,
            'error': f'Sequence length should be at least {block_size} bits'
        }
    return {'is_valid': True}

def validate_ones_proportion(sequence):
    """
    Validates if proportion of ones in sequence is suitable for runs test
    Checks if |π - 0.5| < 2/√n, where π is proportion of ones
    
    Args:
        sequence (list or str): Sequence of bits to validate
        
    Returns:
        dict: Dictionary containing validation result
            {
                'is_valid' (bool): True if proportion of ones is suitable, False otherwise
                'error' (str, optional): Error message if validation failed
            }
    """
    import numpy as np
    n = len(sequence)
    S = sum(sequence)
    pi = S / n
    if abs(pi - 0.5) >= 2 / np.sqrt(n):
        return {
            'is_valid': False,
            'error': 'Test cannot be applied: proportion of ones is too far from 0.5'
        }
    return {'is_valid': True} 