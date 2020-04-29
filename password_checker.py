import sys
import hashlib
import requests


def get_hack_count(query_chars):
    sha1_hash = hash_pass(query_chars)
    response = send_request(sha1_hash)
    hash_list = create_hash_list(response)
    # API responds with hash with 5 first chars discarded
    result = check_pass(hash_list, sha1_hash[5:])
    display_result(query_chars, result)


def hash_pass(password):
    sha1hash = hashlib.sha1(str(password).encode('utf-8')).hexdigest().upper()
    return sha1hash


def send_request(query):
    # sending query with first 5 characters
    url = f'https://api.pwnedpasswords.com/range/{query[:5]}'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res.text


def create_hash_list(response_data):
    hash_list = response_data.splitlines()
    hash_list = map(lambda r: r.split(":"), hash_list)
    return hash_list


def check_pass(hash_list, pass_hash):
    for hash_data in hash_list:
        if pass_hash == hash_data[0]:
            return int(hash_data[1])
    return 0


def display_result(query, num):
    if num:
        print(f"Password '{query}' found!, This password was leaked {num:,} times!")
    else:
        print(f"'{query}' is secure go ahead :)")


def main():
    check_list = sys.argv[1:]
    for pwd in check_list:
        get_hack_count(pwd)


if __name__ == '__main__':
    main()
