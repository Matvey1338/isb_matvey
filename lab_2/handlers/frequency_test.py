import numpy as np
from scipy.special import erfc

def frequency_test(sequence):
    """
    Частотный побитовый тест
    Проверяет, является ли количество нулей и единиц в последовательности примерно равным
    Returns:
        float: p-value
    """
    n = len(sequence)
    
    # Преобразуем последовательность: '1' -> 1, '0' -> -1
    x = np.array([1 if bit == 1 or bit == '1' else -1 for bit in sequence])
    
    # Вычисляем S_N по формуле
    S_N = np.sum(x) / np.sqrt(n)
    
    # Вычисляем p-value через erfc
    return erfc(abs(S_N) / np.sqrt(2)) 