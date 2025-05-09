import numpy as np
from scipy.special import gammaincc

def block_frequency_test(sequence, block_size=8):
    """
    Тест на самую длинную последовательность единиц в блоке (по методичке)
    sequence: список или строка из 0 и 1
    block_size: длина блока (по умолчанию 8)
    """
    # Преобразуем строку в список int, если нужно
    if isinstance(sequence, str):
        sequence = [int(x) for x in sequence]
    n = len(sequence)
    if n < 100:
        return {
            'success': False,
            'message': 'Sequence length should be at least 100 bits',
            'p_value': None
        }
    N = n // block_size
    if N < 1:
        return {
            'success': False,
            'message': f'Sequence length should be at least {block_size} bits',
            'p_value': None
        }
    
    # Обрезаем лишние биты
    sequence = sequence[:N*block_size]
    
    # Теоретические вероятности для блока длиной 8
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
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
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1
    # χ²
    chi2 = sum((v[i] - N * pi[i])**2 / (N * pi[i]) for i in range(4))
    # p-value через неполную гамма-функцию
    p_value = gammaincc(3/2, chi2/2)
    alpha = 0.01
    success = p_value >= alpha
    return {
        'success': success,
        'message': 'Longest run of ones in a block test passed' if success else 'Test failed',
        'p_value': p_value,
        'statistic': chi2,
        'block_size': block_size,
        'number_of_blocks': N,
        'v': v,
        'max_runs': max_runs,
        'theoretical_probabilities': pi
    } 