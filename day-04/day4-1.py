import sys
sys.path.insert(0, '..')

from helpers import filemap

use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
]

inp = [l.split(': ')[1] for l in inp]
inp = [l.split(' | ') for l in inp]
inp = [(tuple(map(int, pair[0].split())), tuple(map(int, pair[1].split()))) for pair in inp]

total_points = 0
for card in inp:
    card_score = 0
    winning_nums = set(card[0])
    for nums in card[1]:
        if nums in winning_nums:
            card_score = 2 * card_score if card_score > 0 else 1
    total_points += card_score

print(total_points)
