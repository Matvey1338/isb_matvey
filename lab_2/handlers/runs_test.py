import numpy as np
from scipy.stats import norm

def runs_test(sequence):
    """
    Тест на одинаковые подряд идущие биты
    Проверяет, является ли количество серий (runs) нулей и единиц случайным
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
    
    # Вычисляем долю единиц
    pi = S / n
    
    # Проверяем условие для применения теста
    if abs(pi - 0.5) >= 2 / np.sqrt(n):
        return {
            'success': False,
            'message': 'Test cannot be applied: proportion of ones is too far from 0.5',
            'p_value': None
        }
    
    # Подсчитываем количество серий
    runs = 1
    for i in range(1, n):
        if sequence[i] != sequence[i-1]:
            runs += 1
    
    # Вычисляем статистику теста
    V_obs = (runs - 2 * n * pi * (1 - pi)) / (2 * np.sqrt(n) * pi * (1 - pi))
    
    # Вычисляем p-value
    p_value = 2 * (1 - norm.cdf(abs(V_obs)))
    
    # Проверяем гипотезу на уровне значимости 0.01
    alpha = 0.01
    success = p_value >= alpha
    
    return {
        'success': success,
        'message': 'Runs test passed' if success else 'Runs test failed',
        'p_value': p_value,
        'statistic': V_obs,
        'runs_count': runs,
        'sequence_length': n,
        'ones_proportion': pi
    } 