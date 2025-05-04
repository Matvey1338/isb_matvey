from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/frequency_test', methods=['POST'])
def frequency_test():
    # TODO: Implement frequency test
    data = request.get_json()
    sequence = data.get('sequence', [])
    return jsonify({'result': 'Frequency test not implemented yet'})

@app.route('/runs_test', methods=['POST'])
def runs_test():
    # TODO: Implement runs test
    data = request.get_json()
    sequence = data.get('sequence', [])
    return jsonify({'result': 'Runs test not implemented yet'})

@app.route('/block_frequency_test', methods=['POST'])
def block_frequency_test():
    # TODO: Implement block frequency test
    data = request.get_json()
    sequence = data.get('sequence', [])
    return jsonify({'result': 'Block frequency test not implemented yet'})

if __name__ == '__main__':
    app.run(debug=True) 