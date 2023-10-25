import argparse
import requests

url = 'http://www.4byte.directory/api/v1/signatures/'


def get_text_signature(hex: str) -> str:
    request = f'{url}?hex_signature={hex}'
    response = requests.get(request)
    return response.json()['results'][0]['text_signature']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--hex', help='Hex Signature that you want to search for')
    args = parser.parse_args()
    print(get_text_signature(args.hex))
