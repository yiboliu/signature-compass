import argparse
import logging
import requests

from server import utils

logging.basicConfig(level=logging.DEBUG,
                    filename='signature_compass_logs.txt',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

url = 'http://www.4byte.directory/api/v1/signatures/'


def get_text_signature(hex: str) -> str:
    """The function is to get the text signature for the given hex signature.
        Args:
            hex: the signature in hex format.
        Returns:
            the text format of the signature.
        Raises:
            ValueError is raised if input is not supported.
    """
    # Per the document of 4bytes, this API only takes the first 4 chars of the signature, with or without 0x as prefix.
    if len(hex) < 8 or (hex.startswith('0x') and len(hex) < 10):
        raise ValueError('the hex string should contains at least 4 chars, with or without prefixing 0x.')
    if hex.startswith('0x'):
        hex = hex[0:10]
    else:
        hex = hex[0:8]
    request = f'{url}?hex_signature={hex}'
    response = requests.get(request)
    # We take the json object of the response and extract the signature to return.
    return response.json()['results'][0]['text_signature']


def _get_request_url(pattern: str, exact: bool, case_sensitive: bool) -> str:
    """This helper function takes the pattern as the given string and check if it contains supported regex.
    exact and case_sensitive are the flags that help determine which API to call as well.
    The corresponding API url to the input string will be returned. """
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
        raise ValueError('regex type unsupported')

    return request_url


def list_signature(text_signature: str, exact: bool = True, case_sensitive: bool = False) -> str:
    """This function is to list the information of the given text_signature.
        Args:
            text_signature: the text signature that is being looked up.
            exact: the flag that determines if this string is looking for exact match, rather than any regex match.
            case_sensitive: the flag that determines whether to be case_sensitive in searching.
        Returns:
            The text format of the response from the http call to the 4bytes server.
    """
    request = _get_request_url(text_signature, exact, case_sensitive)
    response = requests.get(request)
    return response.text


def submit_signature(text_signature: str) -> bool:
    """This function is to submit the text_signature to the 4bytes database upon users' request.
        Args:
            text_signature that is to be submitted.
        Returns:
            The result of submission. True if succeeded and false if failed.
        """
    logger = logging.getLogger('submit.signature')
    # The payload data of the request.
    data = {
        'text_signature': text_signature
    }
    logger.info(f'submitting text signature {text_signature}')
    # Make the http POST call
    response = requests.post(url, json=data)
    if response.ok:
        # If the response is ok, we need to look back to the database to see if it really shows up and matches with
        # input.
        logger.info(f'submitting text signature {text_signature}, status ok. Looking back to 4bytes database to '
                    f'verify...')
        # Take advantage of our existing function to look back to the database.
        lookback = list_signature(text_signature, False, False)
        # If it shows up, then it is guaranteed that submission succeeded.
        if text_signature in lookback:
            logger.info(f'submitting text signature {text_signature}, status ok. Found in 4bytes database')
            return True
        # If we cannot find it, then the submission failed.
        # TODO: in the future, we might want to wait for a while and retry.
        logger.info(f'submitting text signature {text_signature}, status ok. But not found in 4bytes database')
        return False
    # If the response status is not ok, we need to log and return False.
    logger.info(f'submitting text signature {text_signature}, status no ok: {response}')
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--hex', help='Hex Signature that you want to search for')
    args = parser.parse_args()
    print(get_text_signature(args.hex))
