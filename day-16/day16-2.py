import sys
sys.path.insert(0, '..')
sys.setrecursionlimit(8000)

from typing import List, Tuple, Set

from helpers import filemap, CARTESIAN_DIRECTIONS, Vec2D


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
] # 51


def run_beam(
        grid: List[str],
        pos: Vec2D,
        dir: Vec2D,
        visited: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = None,
        energized_tiles: Set[Tuple[int, int]] = None
) -> int:
    if visited is None:
        visited = set()
    if energized_tiles is None:
        energized_tiles = set()

    if (pos, dir) in visited or \
            not (0 <= pos.y < len(grid) and 0 <= pos.x < len(grid[pos.y])):
        return len(energized_tiles)

    energized_tiles.add(pos)
    visited.add((pos, dir))

    tile = grid[pos.y][pos.x]

    if tile == '.':
        next_pos = pos + dir
        next_dir = dir
    elif tile == '/':
        if dir.x == 0:
            next_dir = Vec2D(0, -dir.y)
            next_pos = Vec2D(pos.y, pos.x + next_dir.x)
        else:
            next_dir = Vec2D(-dir.x, 0)
            next_pos = Vec2D(pos.y + next_dir.y, pos.x)
    elif tile == '\\':
        next_dir = Vec2D(dir.x, dir.y)
        next_pos = pos + next_dir
    elif tile == '|':
        if dir.x == 0:
            next_pos = pos + dir
            next_dir = dir
        else:
            return max(
                run_beam(grid, Vec2D(pos.y-1, pos.x), Vec2D(-1, 0), visited, energized_tiles),
                run_beam(grid, Vec2D(pos.y+1, pos.x), Vec2D( 1, 0), visited, energized_tiles)
            )
    elif tile == '-':
        if dir.x == 0:
            return max(
                run_beam(grid, Vec2D(pos.y, pos.x-1), Vec2D(0, -1), visited, energized_tiles),
                run_beam(grid, Vec2D(pos.y, pos.x+1), Vec2D(0,  1), visited, energized_tiles)
            )
        else:
            next_dir = dir
            next_pos = Vec2D(pos.y, pos.x + dir.x)

    return run_beam(grid, next_pos, next_dir, visited, energized_tiles)


max_energized_cnt = 0
max_energized_start = None

def update_energized_count(
        max_energized_cnt: int,
        max_energized_start: Vec2D,
        energized_cnt: int,
        energized_start: Vec2D
):
    if energized_cnt > max_energized_cnt:
        return energized_cnt, energized_start
    return max_energized_cnt, max_energized_start

for y in range(len(inp)):
    start_pos = Vec2D(y, 0)

    et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['E']))
    max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)

    if y == 0:
        et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['S']))
        max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)
    elif y == len(inp)-1:
        et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['N']))
        max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)

    start_pos = Vec2D(y, len(inp[y])-1)
    et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['W']))
    max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)

    if y == 0:
        et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['E']))
        max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)
    elif y == len(inp)-1:
        et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['N']))
        max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)


for x in range(len(inp[0])):
    start_pos = Vec2D(0, x)
    et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['S']))
    max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)

    if x == 0:
        et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['E']))
        max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)
    elif x == len(inp[0])-1:
        et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['W']))
        max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)

    start_pos = Vec2D(len(inp)-1, x)
    et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['N']))
    max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)

    if x == 0:
        et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['E']))
        max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)
    elif x == len(inp[0])-1:
        et = run_beam(inp, start_pos, Vec2D(*CARTESIAN_DIRECTIONS['W']))
        max_energized_cnt, max_energized_start = update_energized_count(max_energized_cnt, max_energized_start, et, start_pos)


print(max_energized_cnt, max_energized_start) # 7438
