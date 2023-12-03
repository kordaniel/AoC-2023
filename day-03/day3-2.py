import sys
sys.path.insert(0, '..')

from helpers import filemap
from typing import List, Tuple, Optional

use_test_data = False

inp = filemap('input.txt') if not use_test_data else [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
] # sum of gear ratios = 467835

def parse_num(l: int, c: int, inp: List[str]) -> Optional[Tuple[int, int]]:
    if not inp[l][c].isdigit():
        return None

    i,j = c, c
    while i-1 >= 0 and inp[l][i-1].isdigit():
        i -= 1
    while j+1 < len(inp[l]) and inp[l][j+1].isdigit():
        j += 1

    return i, j+1 # column boundaries of num


def find_adjacent_nums(l: int, c: int, inp: List[str]) -> List[int]:
    adjacent_nums = []
    for y in range(max(0, l-1), min(l+2, len(inp))):
        x = max(0, c-1)
        while x < min(len(inp[y]), c+2):
            if y == l and x == c:
                x += 1
                continue

            num_idxs = parse_num(y, x, inp)
            if num_idxs is None:
                x += 1
                continue

            adjacent_nums.append(int(inp[y][num_idxs[0]:num_idxs[1]]))
            x = num_idxs[1]

    return adjacent_nums

gear_ratios_sum = 0

for l in range(len(inp)):
    for c in range(len(inp[l])):
        if inp[l][c] == '*':
            adjacent_nums = find_adjacent_nums(l, c, inp)
            if len(adjacent_nums) == 2:
                gear_ratios_sum += adjacent_nums[0] * adjacent_nums[1]

print(gear_ratios_sum)

