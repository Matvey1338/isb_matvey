from .constants import SEQUENCE_LENGTH, BLOCK_SIZE

def validate_sequence_length(sequence):
    """Validates if sequence has correct length"""
    n = len(sequence)
    if n != SEQUENCE_LENGTH:
        return {
            'is_valid': False,
            'error': f'Sequence length should be {SEQUENCE_LENGTH} bits'
        }
    return {'is_valid': True}

def validate_block_size(sequence, block_size=BLOCK_SIZE):
    """Validates if sequence can be divided into blocks"""
    n = len(sequence)
    N = n // block_size
    if N < 1:
        return {
            'is_valid': False,
            'error': f'Sequence length should be at least {block_size} bits'
        }
    return {'is_valid': True}

def validate_ones_proportion(sequence):
    """Validates if proportion of ones is suitable for runs test"""
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