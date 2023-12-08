import sys
sys.path.insert(0, '..')

from typing import List, Tuple, Dict

from helpers import filemap


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    [
        'RL',
        '\n',
        'AAA = (BBB, CCC)',
        'BBB = (DDD, EEE)',
        'CCC = (ZZZ, GGG)',
        'DDD = (DDD, DDD)',
        'EEE = (EEE, EEE)',
        'GGG = (GGG, GGG)',
        'ZZZ = (ZZZ, ZZZ)'
    ], # 2 steps
    [
        'LLR',
        '\n',
        'AAA = (BBB, BBB)',
        'BBB = (AAA, ZZZ)',
        'ZZZ = (ZZZ, ZZZ)'
    ] # 6 steps
][1]


def parse_input(inp: List[str]) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    lines = [tuple(map(str.strip, l.split('='))) for l in inp[2:]]
    lines = [(e[0], e[1][1:-1]) for e in lines]
    lines = dict([(e[0], e[1].split(', ')) for e in lines])
    return inp[0], lines

instructions, node_map = parse_input(inp)


cur_elem = 'AAA'
i = 0
s = 0

while cur_elem != 'ZZZ':
    pick = 0 if instructions[i] == 'L' else 1
    i = 0 if i == len(instructions) - 1 else i + 1
    cur_elem = node_map[cur_elem][pick]
    s += 1

print(s)
