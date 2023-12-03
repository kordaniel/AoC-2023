import sys
sys.path.insert(0, '..')

from helpers import filemap
from typing import List

inp = filemap('input.txt')
#inp = [
#    '467..114..',
#    '...*......',
#    '..35..633.',
#    '......#...',
#    '617*......',
#    '.....+.58.',
#    '..592.....',
#    '......755.',
#    '...$.*....',
#    '.664.598..'
#] # valid parts sum = 4361

def check_if_symbol_adjacent(l: int, c: int, inp: List[str]) -> bool:
    for y in range(max(0, l-1), min(l+2, len(inp))):
        for x in range(max(0, c-1), min(c+2, len(inp[y]))):
            if y == l and x == c:
                continue
            if not inp[y][x].isdigit() and inp[y][x] != '.':
                return True
    return False

part_nums_sum = 0

for l in range(len(inp)):
    col = 0
    while col < len(inp[l]):        
        if not inp[l][col].isdigit():
            col += 1
            continue

        symbol_found = False
        end_col = col
        while True:
            if end_col == len(inp[l]) or not inp[l][end_col].isdigit():
                break
            if not symbol_found and check_if_symbol_adjacent(l, end_col, inp):
                symbol_found = True
            end_col += 1

        if symbol_found:
            part_num = int(inp[l][col:end_col])
            part_nums_sum += part_num
       
        col = end_col 

print(part_nums_sum)

