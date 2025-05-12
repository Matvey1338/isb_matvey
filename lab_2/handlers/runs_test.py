import numpy as np
from scipy.stats import norm
from scipy.special import erfc
from .constants import SEQUENCE_LENGTH

def runs_test(sequence):
    """
    Тест на одинаковые подряд идущие биты
    Проверяет, является ли количество серий (runs) нулей и единиц случайным
    Returns:
        Dictionary containing p_value and raw test data
    """
    n = len(sequence)
    if n != SEQUENCE_LENGTH:
        return {
            'p_value': None,
            'error': f'Sequence length should be {SEQUENCE_LENGTH} bits'
        }
    
    # Вычисляем сумму последовательности (количество единиц)
    S = sum(sequence)
    
    # Вычисляем долю единиц
    pi = S / n
    
    # Проверяем условие для применения теста
    if abs(pi - 0.5) >= 2 / np.sqrt(n):
        return {
            'p_value': None,
            'error': 'Test cannot be applied: proportion of ones is too far from 0.5'
        }
    
    # Подсчитываем количество серий
    runs = 0
    for i in range(1, n):
        if sequence[i] != sequence[i-1]:
            runs += 1
    
    # Вычисляем статистику теста
    V_obs = (runs - 2 * n * pi * (1 - pi)) / (2 * np.sqrt(2 * n) * pi * (1 - pi))
    
    # Вычисляем p-value через функцию ошибок
    p_value = erfc(abs(V_obs))
    
    return {
        'p_value': p_value,
        'statistic': V_obs,
        'runs_count': runs,
        'ones_proportion': pi
    } 