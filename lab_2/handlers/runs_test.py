import numpy as np
from scipy.special import erfc

def runs_test(sequence):
    """
    Тест на одинаковые подряд идущие биты
    Проверяет, является ли количество серий (runs) нулей и единиц случайным
    Returns:
        float: p-value
    """
    n = len(sequence)
    
    # Вычисляем сумму последовательности (количество единиц)
    S = sum(sequence)
    
    # Вычисляем долю единиц
    pi = S / n
    
    # Подсчитываем количество серий
    runs = 0
    for i in range(1, n):
        if sequence[i] != sequence[i-1]:
            runs += 1
    
    # Вычисляем статистику теста
    V_obs = (runs - 2 * n * pi * (1 - pi)) / (2 * np.sqrt(2 * n) * pi * (1 - pi))
    
    # Вычисляем p-value через функцию ошибок
    return erfc(abs(V_obs)) 