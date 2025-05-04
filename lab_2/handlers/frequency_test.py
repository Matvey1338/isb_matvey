import numpy as np
from scipy.stats import norm

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
    
    # Вычисляем сумму последовательности (количество единиц)
    S = sum(sequence)
    
    # Вычисляем статистику теста
    S_obs = abs(S - n/2) / np.sqrt(n/4)
    
    # Вычисляем p-value
    p_value = 2 * (1 - norm.cdf(S_obs))
    
    # Проверяем гипотезу на уровне значимости 0.01
    alpha = 0.01
    success = p_value >= alpha
    
    return {
        'success': success,
        'message': 'Frequency test passed' if success else 'Frequency test failed',
        'p_value': p_value,
        'statistic': S_obs,
        'sequence_length': n,
        'ones_count': S,
        'zeros_count': n - S
    } 