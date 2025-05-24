from flask import Flask, request, jsonify
import logging
from config import Config
from crypto.hybrid import HybridCipher

app = Flask(__name__)
logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')
config = Config()

@app.route('/generate-keys', methods=['POST'])
def generate_keys():
    data = request.json
    size = data.get('sym_key_size', config.key_size)
    paths = data['paths']  # dict: public, private, encrypted_sym
    HybridCipher.generate_all(size, paths['public_key'],
                              paths['private_key'], paths['sym_key'])
    logging.info('Keys generated with sym size %s', size)
    return jsonify(status='ok')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    HybridCipher.encrypt_file(data['input_file'], data['output_file'],
                              data['private_key'], data['sym_key'])
    logging.info('File encrypted: %s', data['output_file'])
    return jsonify(status='ok')

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    HybridCipher.decrypt_file(data['input_file'], data['output_file'],
                              data['private_key'], data['sym_key'])
    logging.info('File decrypted: %s', data['output_file'])
    return jsonify(status='ok')

if __name__ == '__main__':
    app.run(debug=True)