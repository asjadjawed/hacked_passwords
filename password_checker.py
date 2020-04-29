import hashlib

import requests


def request_api_data(query_chars):
    sha1_hash = hash_pass(query_chars)
    url = f'https://api.pwnedpasswords.com/range/{sha1_hash[:5]}'
    res = requests.get(url)
    print(res, res.status_code)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    print(res.text)


def hash_pass(password):
    sha1hash = hashlib.sha1(str(password).encode('utf-8')).hexdigest().upper()
    return sha1hash


def main():
    request_api_data('password')


if __name__ == '__main__':
    main()
