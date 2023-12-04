import sys
sys.path.insert(0, '..')

from helpers import filemap
from typing import Dict, List, Set, Tuple
import time

use_test_data = False


def read_input() -> Dict[int, int]:
    inp = filemap('input.txt') if not use_test_data else [
        'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
        'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
        'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
        'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
        'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
        'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
    ]
    inp = [l.split(': ') for l in inp]
    inp = [(l[0].split()[1], l[1].split(' | ')) for l in inp]
    inp = [(int(pair[0]), list(map(int, pair[1][0].split())), list(map(int, pair[1][1].split())))  for pair in inp]

    cards = dict((c[0], [set(c[1]), c[2]]) for c in inp) # { card_id: [set(winning nums), [card nums]], ... }
    for l in cards.items():
        card_score = 0
        for num in l[1][1]:
            if num in l[1][0]:
                card_score += 1
        l[1].append(card_score)
    card_scores = dict([(c[0], c[1][2]) for c in cards.items()]) # { card_id: matching_nums }
    return card_scores


def count_scratchcards(id: int, scores: Dict[int, int]) -> int:
    count = 1
    for card_id in range(id+1, id+1+scores[id]):
        if not card_id in scores:
            continue
        count += count_scratchcards(card_id, scores)
    return count


def count_cards_bruteforce(card_scores: Dict[int, int]) -> int:
    total_cards = 0

    for card in card_scores.items():
        total_cards += 1 if card[1] == 0 else count_scratchcards(card[0], card_scores)

    return total_cards


def count_cards(card_scores: Dict[int, int]) -> int:
    cards_total = dict([(c[0], dict(zip(range(c[1]), [1 for _ in range(c[1])]))) for c in card_scores.items()])

    for card_id in sorted(cards_total.keys()):
        for next_id in range(card_scores[card_id]):
            n = card_id+next_id+1
            if not n in cards_total:
                continue
            for i in cards_total[n].keys():
                cards_total[n][i] += cards_total[card_id][next_id]

    return sum([sum(c.values()) for c in cards_total.values()]) + len(cards_total)


card_scores = read_input()

if use_test_data:
    time_start = time.time()
    print(count_cards_bruteforce(card_scores))

time_middle = time.time()

print(count_cards(card_scores))
time_end = time.time()

print('Runtimes:')
if use_test_data:
    print('Bruteforce:', time_middle - time_start, 'seconds') # ~3.5s
print('Optimized:', time_end - time_middle, 'seconds')    # 0.001s
