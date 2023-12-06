import sys
sys.path.insert(0, '..')
import re

from helpers import filemap


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    'Time:      7  15   30',
    'Distance:  9  40  200'
] # 288 (4 * 8 * 9)

times = [int(n) for n in re.findall(r'\d+', inp[0].split(':')[1])]
distances = [int(n) for n in re.findall(r'\d+', inp[1].split(':')[1])]

total_wins = 0
for t, d in zip(times, distances):
    options = ((t-ms)*ms for ms in range(1, t))
    winning_options = sum((1 for dist in options if dist > d))

    # Same as above
    #winning_options = 0
    #for ms in range(1, t):
    #    if (t-ms) * ms > d:
    #        winning_options += 1

    if winning_options > 0:
        total_wins = max(total_wins, 1)
        total_wins *= winning_options


print(total_wins)
