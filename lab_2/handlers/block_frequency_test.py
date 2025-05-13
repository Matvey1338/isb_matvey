import numpy as np
from scipy.special import gammaincc
from .constants import THEORETICAL_PROBABILITIES

def block_frequency_test(sequence, block_size=8):
    """
    Тест на самую длинную последовательность единиц в блоке (по методичке)
    sequence: список или строка из 0 и 1
    block_size: длина блока (по умолчанию 8)
    Returns:
        float: p-value
    """
    # Преобразуем строку в список int, если нужно
    if isinstance(sequence, str):
        sequence = [int(x) for x in sequence]
    n = len(sequence)
    N = n // block_size
    
    # Обрезаем лишние биты
    sequence = sequence[:N*block_size]
    
    # v1: макс. длина <=1, v2: =2, v3: =3, v4: >=4
    v = [0, 0, 0, 0]
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
    return gammaincc(3/2, chi2/2) 