from server import signature_compass
from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@app.route('/get-text-signature', methods=['GET'])
def get_text_signature():
    # Get the hex string from the input.
    hex_signature = request.args.get('hex')
    logging.info(f'hex is {hex_signature}')
    # Call the API to get the results
    result = signature_compass.get_text_signature(hex_signature)
    logging.info(f'result is {type(result)}')
    return result


@app.route('/list-signature', methods=['GET'])
def list_signature():
    # Get the text signature from the input.
    text_signature = request.args.get('text')
    if 'exact' in request.args:
        exact_match_input = request.args.get('exact')
        # Convert the value of exact_match to boolean. We only set it to False when the user explicitly do so.
        # Otherwise, we regard it as True as default.
        if exact_match_input.lower() == 'false':
            exact_match = False
        else:
            exact_match = True
    else:
        exact_match = True

    if 'case_sensitive' in request.args:
        # Convert the value of case_sensitive to boolean. We only set it to True when the user explicitly do so.
        # Otherwise, we regard it as False as default. This is to for the most common use cases.
        case_sensitive_input = request.args.get('case_sensitive')
        if case_sensitive_input.lower() == 'true':
            case_sensitive = True
        else:
            case_sensitive = False
    else:
        case_sensitive = False

    logging.info(f'text_signature is {text_signature}')
    # Call the API to get the results.
    result = signature_compass.list_signature(text_signature, exact_match, case_sensitive)
    logging.info(f'result is {type(result)}')
    return result


@app.route('/submit-signature', methods=['POST'])
def submit_signature():
    # Get the hex string from the input.
    signature = request.args.get('signature')
    logging.info(f'The signature to be submitted is {signature}')
    # Call the API to get the results
    result = signature_compass.submit_signature(signature)
    logging.info(f'result is {type(result)}')
    return result


if __name__ == '__main__':
    app.run(debug=True, port=5000)
