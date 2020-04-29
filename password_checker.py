import hashlib

import requests


def get_hack_count(query_chars):
    sha1_hash = hash_pass(query_chars)
    response = send_request(sha1_hash[:5])
    hash_list = create_hash_list(response)
    result = check_pass(hash_list, sha1_hash[5:])
    display_result(query_chars, result)


def display_result(query, num):
    if num:
        print(f"Password '{query}' found!, This password was hacked {num:,} times!")
    else:
        print(f'Password is secure go ahead :)')


def send_request(query):
    url = f'https://api.pwnedpasswords.com/range/{query[:5]}'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res.text


def check_pass(hash_list, pass_hash):
    for hash_data in hash_list:
        if pass_hash == hash_data[0]:
            return int(hash_data[1])
    return 0


def create_hash_list(response_data):
    hash_list = response_data.split('\r\n')
    hash_list = list(map(lambda r: r.split(":"), hash_list))
    return hash_list


def hash_pass(password):
    sha1hash = hashlib.sha1(str(password).encode('utf-8')).hexdigest().upper()
    return sha1hash


def main():
    get_hack_count('spongebob')


if __name__ == '__main__':
    main()
