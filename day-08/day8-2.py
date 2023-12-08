import sys
sys.path.insert(0, '..')

import math
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
        #'CCD = (EEE, DDD)', #
        'EEE = (EEE, EEE)',
        #'BBA = (AAA, BBB)', #
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
][0]


def parse_input(inp: List[str]) -> Tuple[str, List[str], Dict[str, Tuple[str, str]]]:
    nodes_maps = {}

    lines = [tuple(map(str.strip, l.split('='))) for l in inp[2:]]
    lines = [(e[0], e[1][1:-1]) for e in lines]
    lines = [(e[0], e[1].split(', ')) for e in lines]

    for l in lines:
        if l[-1] == 'Z':
            continue
        prefix, end_char = l[0][:2], l[0][2]

        cnts = nodes_maps.get(end_char, {})
        if prefix in cnts:
            continue
        cnts[prefix] = 10 + len(cnts)
        nodes_maps[end_char] = cnts

    def map_loc(loc: str) -> str:
        prefix, end = loc[:2], loc[2]
        if end == 'Z':
            return 'XXX'
        return ''.join((str(nodes_maps[end][prefix]), end))

    mapped_lines = []
    for l in lines:
        if l[-1] == 'Z':
            mapped_lines.append(('XXX', l[1]))
            continue

        node_src = map_loc(l[0])
        left     = map_loc(l[1][0])
        right    = map_loc(l[1][1])
        mapped_lines.append((node_src, (left, right)))

    lines = dict(mapped_lines)
    starting_nodes = [f'{prefix}A' for prefix in nodes_maps['A'].values()]

    return inp[0], starting_nodes, lines


def find_moves_cnt(
    start_node: str,
    instructions: str,
    node_map: Dict[str, Tuple[str, str]]
) -> Tuple[int, int]:
    i = 0
    steps = 0
    steps_first, steps_seconds = None, None
    cur = start_node

    while True:
        pick = 0 if instructions[i] == 'L' else 1
        i = 0 if i == len(instructions)-1 else i+1
        steps += 1

        cur = node_map[cur][pick]

        if cur == 'XXX':
            if steps_first == None:
                steps_first = steps
                steps = 0
            else:
                steps_second = steps
                break

    return steps_first, steps_second


def compute_lcm(nums: List[int]) -> int:
    # Python 3.8 math library does not contain lcm function
    lcm = nums[0]
    for n in nums[1:]:
        gcd = math.gcd(lcm, n)
        lcm = (lcm * n) // gcd

    return lcm


instructions, nodes, node_map = parse_input(inp)
steps = [find_moves_cnt(node, instructions, node_map) for node in nodes]
# steps = [(initial step count A->Z, cycle step count Z->Z)), (..), ..]

print(compute_lcm([e[0] for e in steps]))
