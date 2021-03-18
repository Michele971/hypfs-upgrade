import requests
from src.parameters import *


def request(neighbor, operation, params):
    url = "http://{}:{}/{}".format(LOCAL_HOST, str(int(neighbor, 2) + INIT_PORT), operation)
    return requests.get(url=url, params=params)


def create_binary_id(n):
    binary_id = bin(n)[2:]
    while len(binary_id) < HYPERCUBE_SIZE:
        binary_id = '0' + binary_id
    return binary_id


def hamming_distance(n1, n2):
    x = n1 ^ n2
    set_bits = 0
    while x > 0:
        set_bits += x & 1
        x >>= 1
    return set_bits
