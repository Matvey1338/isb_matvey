import numpy as np
from scipy.stats import norm
from scipy.special import erfc
from .constants import SEQUENCE_LENGTH

def frequency_test(sequence):
    """
    Частотный побитовый тест
    Проверяет, является ли количество нулей и единиц в последовательности примерно равным
    Returns:
        Dictionary containing p_value and raw test data
    """
    n = len(sequence)
    if n != SEQUENCE_LENGTH:
        return {
            'p_value': None,
            'error': f'Sequence length should be {SEQUENCE_LENGTH} bits'
        }
    
    # Преобразуем последовательность: '1' -> 1, '0' -> -1
    x = np.array([1 if bit == 1 or bit == '1' else -1 for bit in sequence])
    
    # Вычисляем S_N по формуле
    S_N = np.sum(x) / np.sqrt(n)
    
    # Вычисляем p-value через erfc
    p_value = erfc(abs(S_N) / np.sqrt(2))
    
    return {
        'p_value': p_value,
        'statistic': S_N,
        'sequence_length': n,
        'ones_count': int(np.sum(x == 1)),
        'zeros_count': int(np.sum(x == -1))
    } 