import sys
sys.path.insert(0, '..')

from helpers import filemap


use_test_data = False
inp = filemap('input.txt', sep=',') if not use_test_data else [
    'rn=1',
    'cm-',
    'qp=3',
    'cm=2',
    'qp-',
    'pc=4',
    'ot=9',
    'ab=5',
    'pc-',
    'pc=6',
    'ot=7'
] # 1320


def compute_hash(inp_string: str) -> int:
    result = 0
    for c in (ord(c) for c in inp_string):
        result += c
        result *= 17
        result %= 256
    return result

hashes_sum = sum(compute_hash(step) for step in inp)
print(hashes_sum)
