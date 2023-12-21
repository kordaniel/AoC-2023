import sys
sys.path.insert(0, '..')

from typing import List, Set, Tuple

from helpers import filemap, CartesianDir


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........'
]

H, W = len(inp), len(inp[0])


def dfs(
        inp: List[str],
        pos: Tuple[int, int],
        visited: Set[Tuple[int, int]],
        end_positions: Set[Tuple[int, int]],
        steps_left: int
) -> int:
    position_state = (steps_left, *pos)

    if steps_left == 0:
        end_positions.add(pos)
        return len(end_positions)

    elif position_state in visited:
        return 0

    visited.add(position_state)

    cnt = 0
    for dir in (CartesianDir.N, CartesianDir.E, CartesianDir.S, CartesianDir.W):
        next_pos = pos[0] + dir.value[0], pos[1] + dir.value[1]

        if not (0 <= next_pos[0] < H and 0 <= next_pos[1] < W):
            continue
        elif inp[next_pos[0]][next_pos[1]] == '#':
            continue

        cnt = max(cnt, dfs(inp, next_pos, visited, end_positions, steps_left-1))

    return cnt


start_positions = tuple((r,c) for r in range(H) for c in range(W) if inp[r][c] == 'S')
steps = 64

print(dfs(inp, start_positions[0], set(), set(), steps))
