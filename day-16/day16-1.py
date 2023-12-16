import sys
sys.path.insert(0, '..')
sys.setrecursionlimit(8000)
from typing import List, Tuple

from helpers import filemap, CARTESIAN_DIRECTIONS


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    '.|...\....',
    '|.-.\.....',
    '.....|-...',
    '........|.',
    '..........',
    '.........\\',
    '..../.\\\\..',
    '.-.-/..|..',
    '.|....-|.\\',
    '..//.|....'
] # 46

energized_tiles = set()
visited = set()

def run_beam(grid: List[str], pos: Tuple[int, int], dir: Tuple[int, int]):
    if pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return
    elif (pos, dir) in visited:
        return

    energized_tiles.add(pos)
    visited.add((pos, dir))
    if len(energized_tiles) == len(grid) * len(grid[pos[0]]):
        return # All tiles visited

    tile = grid[pos[0]][pos[1]]
    
    if tile == '.':
        next_pos = pos[0] + dir[0], pos[1] + dir[1]
        next_dir = dir
    elif tile == '/':
        if dir[0] == -1:
            next_pos = pos[0], pos[1] + 1
            next_dir = 0, 1
        elif dir[0] == 1:
            next_pos = pos[0], pos[1] - 1
            next_dir = 0, -1
        else:
            if dir[1] == -1:
                next_pos = pos[0] + 1, pos[1]
                next_dir = 1, 0
            elif dir[1] == 1:
                next_pos = pos[0] - 1, pos[1]
                next_dir = -1, 0
            else:
                print('invalid direction')
                return
    elif tile == '\\':
        if dir[0] == -1:
            next_pos = pos[0], pos[1] - 1
            next_dir = 0, -1
        elif dir[0] == 1:
            next_pos = pos[0], pos[1] + 1
            next_dir = 0, 1
        else:
            if dir[1] == -1:
                next_pos = pos[0] - 1, pos[1]
                next_dir = -1, 0
            elif dir[1] == 1:
                next_pos = pos[0] + 1, pos[1]
                next_dir = 1, 0
            else:
                print('invalid direction')
                return
    elif tile == '|':
        if dir[0] == -1:
            next_pos = pos[0] - 1, pos[1]
            next_dir = dir
        elif dir[0] == 1:
            next_pos = pos[0] + 1, pos[1]
            next_dir = dir
        else:
            if dir[1] == -1 or dir[1] == 1:
                run_beam(grid, (pos[0]-1, pos[1]), (-1, 0))
                run_beam(grid, (pos[0]+1, pos[1]), ( 1, 0))
                return
            else:
                print('invalid direction')
                return
    elif tile == '-':
        if dir[0] == -1 or dir[0] == 1:
            run_beam(grid, (pos[0], pos[1]-1), (0, -1))
            run_beam(grid, (pos[0], pos[1]+1), (0,  1))
            return
        else:
            if dir[1] == -1:
                next_pos = pos[0], pos[1] - 1
                next_dir = dir
            elif dir[1] == 1:
                next_pos = pos[0], pos[1] + 1
                next_dir = dir
            else:
                print('invalid direction')
                return

    run_beam(grid, next_pos, next_dir)

run_beam(inp, (0, 0), (0, 1))
print(len(energized_tiles))
