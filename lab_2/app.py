from flask import Flask, render_template, request, jsonify
import numpy as np
from handlers.frequency_test import frequency_test
from handlers.runs_test import runs_test
from handlers.block_frequency_test import block_frequency_test
from handlers.test_result_processor import process_test_result
from handlers.validations import validate_sequence_length, validate_ones_proportion, validate_block_size
from handlers.config import BLOCK_SIZE, THEORETICAL_PROBABILITIES

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/frequency_test', methods=['POST'])
def frequency_test_handler():
    data = request.get_json()
    sequence = data.get('sequence', [])
    
    # Validate sequence length
    validation = validate_sequence_length(sequence)
    if not validation['is_valid']:
        return jsonify(process_test_result('Frequency test', None, validation))
    
    # Calculate p-value
    p_value = frequency_test(sequence)
    
    # Prepare additional data for frontend
    x = np.array([1 if bit == 1 or bit == '1' else -1 for bit in sequence])
    additional_data = {
        'statistic': np.sum(x) / np.sqrt(len(sequence)),
        'sequence_length': len(sequence),
        'ones_count': int(np.sum(x == 1)),
        'zeros_count': int(np.sum(x == -1))
    }
    
    result = process_test_result('Frequency test', p_value, additional_data)
    result['success'] = str(result['success'])
    return jsonify(result)

@app.route('/runs_test', methods=['POST'])
def runs_test_handler():
    data = request.get_json()
    sequence = data.get('sequence', [])
    
    # Validate sequence length
    validation = validate_sequence_length(sequence)
    if not validation['is_valid']:
        return jsonify(process_test_result('Runs test', None, validation))
    
    # Validate ones proportion
    validation = validate_ones_proportion(sequence)
    if not validation['is_valid']:
        return jsonify(process_test_result('Runs test', None, validation))
    
    # Calculate p-value
    p_value = runs_test(sequence)
    
    # Prepare additional data for frontend
    n = len(sequence)
    S = sum(sequence)
    pi = S / n
    runs = 0
    for i in range(1, n):
        if sequence[i] != sequence[i-1]:
            runs += 1
    
    V_obs = (runs - 2 * n * pi * (1 - pi)) / (2 * np.sqrt(2 * n) * pi * (1 - pi))
    additional_data = {
        'statistic': V_obs,
        'runs_count': runs,
        'ones_proportion': pi
    }
    
    result = process_test_result('Runs test', p_value, additional_data)
    result['success'] = str(result['success'])
    return jsonify(result)

@app.route('/block_frequency_test', methods=['POST'])
def block_frequency_test_handler():
    data = request.get_json()
    sequence = data.get('sequence', [])
    
    # Validate sequence length
    validation = validate_sequence_length(sequence)
    if not validation['is_valid']:
        return jsonify(process_test_result('Block frequency test', None, validation))
    
    # Validate block size
    validation = validate_block_size(sequence)
    if not validation['is_valid']:
        return jsonify(process_test_result('Block frequency test', None, validation))
    
    # Calculate p-value
    p_value = block_frequency_test(sequence)
    
    # Prepare additional data for frontend
    n = len(sequence)
    N = n // BLOCK_SIZE
    sequence = sequence[:N*BLOCK_SIZE]
    
    v = [0, 0, 0, 0]
    max_runs = []
    for i in range(N):
        block = sequence[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE]
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
    
    chi2 = sum((v[i] - N * THEORETICAL_PROBABILITIES[i])**2 / (N * THEORETICAL_PROBABILITIES[i]) for i in range(4))
    
    additional_data = {
        'statistic': chi2,
        'sequence_length': n,
        'block_size': BLOCK_SIZE,
        'number_of_blocks': N,
        'v': v,
        'max_runs': max_runs,
        'theoretical_probabilities': THEORETICAL_PROBABILITIES
    }
    
    result = process_test_result('Block frequency test', p_value, additional_data)
    result['success'] = str(result['success'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 