import numpy as np
from scipy.stats import norm
from scipy.special import erfc

def frequency_test(sequence):
    """
    Частотный побитовый тест
    Проверяет, является ли количество нулей и единиц в последовательности примерно равным
    """
    n = len(sequence)
    if n < 100:
        return {
            'success': False,
            'message': 'Sequence length should be at least 100 bits',
            'p_value': None
        }
    
    # Преобразуем последовательность: '1' -> 1, '0' -> -1
    x = np.array([1 if bit == 1 or bit == '1' else -1 for bit in sequence])
    
    # Вычисляем S_N по формуле
    S_N = np.sum(x) / np.sqrt(n)
    
    # Вычисляем p-value через erfc
    p_value = erfc(abs(S_N) / np.sqrt(2))
    
    # Проверяем гипотезу на уровне значимости 0.01
    alpha = 0.01
    success = p_value >= alpha
    
    return {
        'success': success,
        'message': 'Frequency test passed' if success else 'Frequency test failed',
        'p_value': p_value,
        'statistic': S_N,
        'sequence_length': n,
        'ones_count': int(np.sum(x == 1)),
        'zeros_count': int(np.sum(x == -1))
    } 