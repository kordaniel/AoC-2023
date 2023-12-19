import sys
sys.path.insert(0, '..')
sys.setrecursionlimit(8000)

from typing import Callable, List, Set, Tuple

from helpers import filemap, Vec2D, CartesianDir


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


def beam(
        grid: List[str],
        pos: Vec2D,
        dir: CartesianDir
) -> int:
    # computes the same result as run_beam
    dirmap = {
        CartesianDir.N: 0,
        CartesianDir.E: 1,
        CartesianDir.S: 2,
        CartesianDir.W: 3
    }

    stack: List[Tuple[int, int, int]] = [(*pos.get_coords(), dirmap[dir])] # (y, x, direction)
    visited = set()
    energized_tiles = set()

    while len(stack) != 0:
        posdir = stack.pop()

        if posdir in visited or \
                not (0 <= posdir[0] < len(grid) and 0 <= posdir[1] < len(grid[posdir[0]])):
            continue

        pos, dir = posdir[:2], posdir[2]

        energized_tiles.add(pos)
        visited.add(posdir)

        tile = grid[pos[0]][pos[1]]

        if tile == '|':
            if dir == 1 or dir == 3:
                stack.append((pos[0]-1, pos[1], 0))
                stack.append((pos[0]+1, pos[1], 2))
                continue
        elif tile == '-':
            if dir == 0 or dir == 2:
                stack.append((pos[0], pos[1]-1, 3))
                stack.append((pos[0], pos[1]+1, 1))
                continue

        if tile == '/':
            if dir == 0:
                dir = 1
            elif dir == 2:
                dir = 3
            elif dir == 3:
                dir = 2
            elif dir == 1:
                dir = 0
        elif tile == '\\':
            if dir == 0:
                dir = 3
            elif dir == 2:
                dir = 1
            elif dir == 3:
                dir = 0
            elif dir == 1:
                dir = 2

        if dir == 0:
            stack.append((pos[0]-1, pos[1], dir))
        elif dir == 1:
            stack.append((pos[0], pos[1]+1, dir))
        elif dir == 2:
            stack.append((pos[0]+1, pos[1], dir))
        elif dir == 3:
            stack.append((pos[0], pos[1]-1, dir))

    return len(energized_tiles)


def run_beam(
        grid: List[str],
        pos: Vec2D,
        dir: CartesianDir,
        visited: Set[Tuple[Tuple[int, int], Tuple[int, int]]] = None,
        energized_tiles: Set[Tuple[int, int]] = None
) -> int:
    # computes the same result as beam
    if visited is None:
        visited = set()
    if energized_tiles is None:
        energized_tiles = set()

    if (pos.get_coords(), dir) in visited or \
            not (0 <= pos.y < len(grid) and 0 <= pos.x < len(grid[pos.y])):
        return len(energized_tiles)

    energized_tiles.add(pos.get_coords())
    visited.add((pos.get_coords(), dir))

    tile = grid[pos.y][pos.x]

    if tile == '|':
        if dir.value[0] == 0:
            return max(
                run_beam(grid, Vec2D(pos.y-1, pos.x), CartesianDir.N, visited, energized_tiles),
                run_beam(grid, Vec2D(pos.y+1, pos.x), CartesianDir.S, visited, energized_tiles)
            )
    elif tile == '-':
        if dir.value[1] == 0:
            return max(
                run_beam(grid, Vec2D(pos.y, pos.x-1), CartesianDir.W, visited, energized_tiles),
                run_beam(grid, Vec2D(pos.y, pos.x+1), CartesianDir.E, visited, energized_tiles)
            )

    if tile == '/':
        dir = {
            CartesianDir.N: CartesianDir.E,
            CartesianDir.S: CartesianDir.W,
            CartesianDir.E: CartesianDir.N,
            CartesianDir.W: CartesianDir.S
        }[dir]
    elif tile == '\\':
        dir = {
            CartesianDir.N: CartesianDir.W,
            CartesianDir.S: CartesianDir.E,
            CartesianDir.W: CartesianDir.N,
            CartesianDir.E: CartesianDir.S
        }[dir]

    pos.transform(dir)
    return run_beam(grid, pos, dir, visited, energized_tiles)


def update_energized_count(
        max_energized_cnt: int,
        max_energized_start: Vec2D,
        energized_cnt: int,
        energized_start: Vec2D
) -> Tuple[int, Vec2D]:
    if energized_cnt > max_energized_cnt:
        return energized_cnt, energized_start
    return max_energized_cnt, max_energized_start


def run_beams_rows(
        inp: List[str],
        counter_func: Callable[[List[str], Vec2D, CartesianDir], int]
) -> Tuple[int, Vec2D]:
    max_energized_cnt = 0
    max_energized_start = None

    for y in range(len(inp)):
        start_pos = Vec2D(y, 0)

        et = counter_func(inp, start_pos, CartesianDir.E)
        max_energized_cnt, max_energized_start = update_energized_count(
            max_energized_cnt, max_energized_start, et, start_pos
        )

        if y == 0:
            et = counter_func(inp, start_pos, CartesianDir.S)
            max_energized_cnt, max_energized_start = update_energized_count(
                max_energized_cnt, max_energized_start, et, start_pos
            )
        elif y == len(inp)-1:
            et = counter_func(inp, start_pos, CartesianDir.N)
            max_energized_cnt, max_energized_start = update_energized_count(
                max_energized_cnt, max_energized_start, et, start_pos
            )

        start_pos = Vec2D(y, len(inp[y])-1)
        et = counter_func(inp, start_pos, CartesianDir.W)
        max_energized_cnt, max_energized_start = update_energized_count(
            max_energized_cnt, max_energized_start, et, start_pos
        )

        if y == 0:
            et = counter_func(inp, start_pos, CartesianDir.E)
            max_energized_cnt, max_energized_start = update_energized_count(
                max_energized_cnt, max_energized_start, et, start_pos
            )
        elif y == len(inp)-1:
            et = counter_func(inp, start_pos, CartesianDir.N)
            max_energized_cnt, max_energized_start = update_energized_count(
                max_energized_cnt, max_energized_start, et, start_pos
            )

    return max_energized_cnt, max_energized_start


def run_beams_cols(
        inp: List[str],
        counter_func: Callable[[List[str], Vec2D, CartesianDir], int]
) -> Tuple[int, Vec2D]:
    max_energized_cnt = 0
    max_energized_start = None

    for x in range(len(inp[0])):
        start_pos = Vec2D(0, x)
        et = counter_func(inp, start_pos, CartesianDir.S)
        max_energized_cnt, max_energized_start = update_energized_count(
            max_energized_cnt, max_energized_start, et, start_pos
        )

        if x == 0:
            et = counter_func(inp, start_pos, CartesianDir.E)
            max_energized_cnt, max_energized_start = update_energized_count(
                max_energized_cnt, max_energized_start, et, start_pos
            )
        elif x == len(inp[0])-1:
            et = counter_func(inp, start_pos, CartesianDir.W)
            max_energized_cnt, max_energized_start = update_energized_count(
                max_energized_cnt, max_energized_start, et, start_pos
            )

        start_pos = Vec2D(len(inp)-1, x)
        et = counter_func(inp, start_pos, CartesianDir.N)
        max_energized_cnt, max_energized_start = update_energized_count(
            max_energized_cnt, max_energized_start, et, start_pos
        )

        if x == 0:
            et = counter_func(inp, start_pos, CartesianDir.E)
            max_energized_cnt, max_energized_start = update_energized_count(
                max_energized_cnt, max_energized_start, et, start_pos
            )
        elif x == len(inp[0])-1:
            et = counter_func(inp, start_pos, CartesianDir.W)
            max_energized_cnt, max_energized_start = update_energized_count(
                max_energized_cnt, max_energized_start, et, start_pos
            )

    return max_energized_cnt, max_energized_start


# The recursive run_beam function is ~4x slower than the stack based beam function.
# Both are about 3x slower when using classes (current implementation) than when using simple
# tuples and integers as in Part I solution
rows_max_energized_cnt, rows_max_energized_start = run_beams_rows(inp, beam)
cols_max_energized_cnt, cols_max_energized_start = run_beams_cols(inp, beam)

if rows_max_energized_cnt > cols_max_energized_cnt:
    print(rows_max_energized_cnt, rows_max_energized_start)
else:
    print(cols_max_energized_cnt, cols_max_energized_start)
