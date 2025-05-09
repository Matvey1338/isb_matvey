from flask import Flask, render_template, request, jsonify
import numpy as np
from handlers.frequency_test import frequency_test
from handlers.runs_test import runs_test
from handlers.block_frequency_test import block_frequency_test

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/frequency_test', methods=['POST'])
def frequency_test_handler():
    data = request.get_json()
    sequence = data.get('sequence', [])
    result = frequency_test(sequence)
    result['success'] = str(result['success'])
    return jsonify(result)

@app.route('/runs_test', methods=['POST'])
def runs_test_handler():
    data = request.get_json()
    sequence = data.get('sequence', [])
    result = runs_test(sequence)
    result['success'] = str(result['success'])
    return jsonify(result)

@app.route('/block_frequency_test', methods=['POST'])
def block_frequency_test_handler():
    data = request.get_json()
    sequence = data.get('sequence', [])
    result = block_frequency_test(sequence)
    result['success'] = str(result['success'])
    result['sequence_length'] = len(sequence)
    response = {
        'success': result['success'],
        'message': result['message'],
        'p_value': result['p_value'],
        'statistic': result['statistic'],
        'sequence_length': result['number_of_blocks'] * result['block_size'],
        'block_size': result['block_size'],
        'number_of_blocks': result['number_of_blocks'],
        'v': result['v'],
        'max_runs': result['max_runs'],
        'theoretical_probabilities': result['theoretical_probabilities']
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True) 