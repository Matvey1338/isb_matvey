import numpy as np
from scipy.special import gammaincc
from .constants import SEQUENCE_LENGTH, BLOCK_SIZE, THEORETICAL_PROBABILITIES

def block_frequency_test(sequence, block_size=BLOCK_SIZE):
    """
    Тест на самую длинную последовательность единиц в блоке (по методичке)
    sequence: список или строка из 0 и 1
    block_size: длина блока (по умолчанию 8)
    Returns:
        Dictionary containing p_value and raw test data
    """
    # Преобразуем строку в список int, если нужно
    if isinstance(sequence, str):
        sequence = [int(x) for x in sequence]
    n = len(sequence)
    if n != SEQUENCE_LENGTH:
        return {
            'p_value': None,
            'error': f'Sequence length should be {SEQUENCE_LENGTH} bits'
        }
    N = n // block_size
    if N < 1:
        return {
            'p_value': None,
            'error': f'Sequence length should be at least {block_size} bits'
        }
    
    # Обрезаем лишние биты
    sequence = sequence[:N*block_size]
    
    # v1: макс. длина <=1, v2: =2, v3: =3, v4: >=4
    v = [0, 0, 0, 0]
    max_runs = []
    for i in range(N):
        block = sequence[i*block_size:(i+1)*block_size]
        # ищем максимальную длину подряд идущих единиц
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == 1:
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0
        max_runs.append(max_run)
        
        match max_run:
            case run if run <= 1:
                v[0] += 1
            case 2:
                v[1] += 1
            case 3:
                v[2] += 1
            case _:
                v[3] += 1
                
    # χ²
    chi2 = sum((v[i] - N * THEORETICAL_PROBABILITIES[i])**2 / (N * THEORETICAL_PROBABILITIES[i]) for i in range(4))
    # p-value через неполную гамма-функцию
    p_value = gammaincc(3/2, chi2/2)
    
    return {
        'p_value': p_value,
        'statistic': chi2,
        'block_size': block_size,
        'number_of_blocks': N,
        'v': v,
        'max_runs': max_runs,
        'theoretical_probabilities': THEORETICAL_PROBABILITIES
    } 