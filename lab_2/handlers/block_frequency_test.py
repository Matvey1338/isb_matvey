import numpy as np
from scipy.stats import chi2

def block_frequency_test(sequence, block_size=128):
    """
    Тест на самую длинную последовательность единиц в блоке
    Проверяет частоту единиц в блоках фиксированного размера
    """
    n = len(sequence)
    if n < 100:
        return {
            'success': False,
            'message': 'Sequence length should be at least 100 bits',
            'p_value': None
        }
    
    # Определяем количество блоков
    N = n // block_size
    if N < 1:
        return {
            'success': False,
            'message': f'Sequence length should be at least {block_size} bits',
            'p_value': None
        }
    
    # Вычисляем частоту единиц в каждом блоке
    block_frequencies = []
    for i in range(N):
        block = sequence[i*block_size:(i+1)*block_size]
        block_frequencies.append(sum(block) / block_size)
    
    # Вычисляем статистику теста
    chi_square = 4 * block_size * sum((freq - 0.5)**2 for freq in block_frequencies)
    
    # Вычисляем p-value
    p_value = 1 - chi2.cdf(chi_square, N)
    
    # Проверяем гипотезу на уровне значимости 0.01
    alpha = 0.01
    success = p_value >= alpha
    
    return {
        'success': success,
        'message': 'Block frequency test passed' if success else 'Block frequency test failed',
        'p_value': p_value,
        'statistic': chi_square,
        'block_size': block_size,
        'number_of_blocks': N,
        'block_frequencies': block_frequencies
    } 