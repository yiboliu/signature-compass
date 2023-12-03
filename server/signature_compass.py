import argparse
import logging
import requests

import utils

logging.basicConfig(level=logging.DEBUG,
                    filename='signature_compass_logs.txt',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

url = 'http://www.4byte.directory/api/v1/signatures/'


def get_text_signature(hex: str) -> str:
    request = f'{url}?hex_signature={hex}'
    response = requests.get(request)
    return response.json()['results'][0]['text_signature']


def get_request_url(pattern: str, exact: bool, case_sensitive: bool) -> str:
    request_url = f'{url}?text_signature'
    if exact:
        return request_url + '__iexact'
    regex_type = utils.analyze_regex(pattern)
    if regex_type == utils.RegexType.START:
        if case_sensitive:
            request_url += '__istartswith'
        else:
            request_url += '__startswith'
    elif regex_type == utils.RegexType.END:
        if case_sensitive:
            request_url += '__iendswith'
        else:
            request_url += '__endswith'
    elif regex_type == utils.RegexType.CONTAIN:
        if case_sensitive:
            request_url += '__icontains'
        else:
            request_url += '__contains'
    else:
        raise Exception('regex type unsupported')


def list_signatures(text_signature: str, exact: bool, case_sensitive: bool = False) -> str:
    request = get_request_url(text_signature, exact, case_sensitive)
    response = requests.get(request)
    return response.text


def submit_signature(text_signature: str) -> bool:
    logger = logging.getLogger('submit.signature')
    data = {
        'text_signature': text_signature
    }
    logger.info(f'submitting text signature {text_signature}')
    response = requests.post(url, json=data)
    if response.ok:
        logger.info(f'submitting text signature {text_signature}, status ok. Looking back to 4bytes database to '
                    f'verify...')
        lookback = list_signatures(text_signature, False, False)
        if text_signature in lookback:
            logger.info(f'submitting text signature {text_signature}, status ok. Found in 4bytes database')
            return True
        logger.info(f'submitting text signature {text_signature}, status ok. But not found in 4bytes database')
        return False
    logger.info(f'submitting text signature {text_signature}, status no ok: {response}')
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--hex', help='Hex Signature that you want to search for')
    args = parser.parse_args()
    print(get_text_signature(args.hex))
