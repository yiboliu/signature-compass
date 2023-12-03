from server import signature_compass
from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@app.route('/get-text-signature', methods=['GET'])
def get_text_signature():
    hex_signature = request.args.get('hex')
    logging.info(f'hex is {hex_signature}')
    result = signature_compass.get_text_signature(hex_signature)
    logging.info(f'result is {type(result)}')
    return result


if __name__ == '__main__':
    app.run(debug=True, port=5000)
