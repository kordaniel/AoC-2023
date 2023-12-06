import sys
sys.path.insert(0, '..')
import re

from helpers import filemap


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    'Time:      7  15   30',
    'Distance:  9  40  200'
] # 71503 (14 to 71516) ways


time = re.findall('\d+', inp[0].split(':')[1])
time = int(''.join(time))

distance = re.findall('\d+', inp[1].split(':')[1])
distance = int(''.join(distance))


def compute_ways_bruteforce(time: int, distance: int) -> int:
    solutions = 0
    for ms in range(1, time):
        if (time-ms) * ms > distance:
            solutions += 1
    return solutions


def compute_ways_optimized(time: int, distance: int) -> int:
    k = 0
    i = time//2
    while i > 0:
        while (time-(k+i)) * (k+i) < distance:
            k += i
        i //= 2
    return time-2*k-1


#print(compute_ways_bruteforce(time, distance)) # ~6s
print(compute_ways_optimized(time, distance))   # ~0.1s
