import sys
sys.path.insert(0, '..')

from typing import Tuple

from helpers import filemap


use_test_data = False
inp = filemap('input.txt', lambda l: tuple(map(int, l.split()))) if not use_test_data else [
    (0, 3, 6, 9, 12, 15),
    (1, 3, 6, 10, 15, 21),
    (10, 13, 16, 21, 30, 45)
] # 2


def predict_next(seq: Tuple[int]) -> int:
    return (
        0 if all(n == 0 for n in seq)
        else seq[-1] + predict_next(tuple(n-seq[i] for i, n in enumerate(seq[1:])))
    )

def predict_prev(seq: Tuple[int]) -> int:
    return predict_next(seq[::-1])


print(sum(predict_prev(seq) for seq in inp))
