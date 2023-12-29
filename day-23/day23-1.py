import sys
sys.path.insert(0, '..')
sys.setrecursionlimit(8000)


from typing import List, Set, Tuple

from helpers import filemap, CartesianDir


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    '#.#####################',
    '#.......#########...###',
    '#######.#########.#.###',
    '###.....#.>.>.###.#.###',
    '###v#####.#v#.###.#.###',
    '###.>...#.#.#.....#...#',
    '###v###.#.#.#########.#',
    '###...#.#.#.......#...#',
    '#####.#.#.#######.#.###',
    '#.....#.#.#.......#...#',
    '#.#####.#.#.#########v#',
    '#.#...#...#...###...>.#',
    '#.#.#v#######v###.###v#',
    '#...#.>.#...>.>.#.###.#',
    '#####v#.#.###v#.#.###.#',
    '#.....#...#...#.#.#...#',
    '#.#########.###.#.#.###',
    '#...###...#...#...#.###',
    '###.###.#.###v#####v###',
    '#...#...#.#.>.>.#.>.###',
    '#.###.###.#.###.#.#v###',
    '#.....###...###...#...#',
    '#####################.#'
] # 94, 90, 86, 82, 82, 74

H, W = len(inp), len(inp[0])


def find_start_end_positions(inp: List[str]) -> List[Tuple[int, int]]:
    start = tuple((0, c) for c in range(W) if inp[0][c] == '.')
    end   = tuple((H-1, c) for c in range(W) if inp[H-1][c] == '.')
    return [*start, *end]


def in_bounds(pos: Tuple[int, int]) -> bool:
    return 0 <= pos[0] < H and 0 <= pos[1] < W


def next_coords(inp: List[str], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    coords_lst = list()

    for dir in (CartesianDir.N, CartesianDir.E, CartesianDir.S, CartesianDir.W):
        next_pos = pos[0] + dir.value[0], pos[1] + dir.value[1]
        if not in_bounds(next_pos):
            continue
        elif inp[next_pos[0]][next_pos[1]] == '#':
            continue
        elif inp[next_pos[0]][next_pos[1]] == '^' and dir != CartesianDir.N:
            continue
        elif inp[next_pos[0]][next_pos[1]] == '>' and dir != CartesianDir.E:
            continue
        elif inp[next_pos[0]][next_pos[1]] == 'v' and dir != CartesianDir.S:
            continue
        elif inp[next_pos[0]][next_pos[1]] == '<' and dir != CartesianDir.W:
            continue
        coords_lst.append(next_pos)

    return coords_lst


def dfs(inp: List[str], pos: Tuple[int, int], end_pos: Tuple[int, int], steps: int, visited: Set[Tuple[int, int]]) -> int:
    if pos == end_pos:
        return steps

    path_steps = 0

    for next_pos in next_coords(inp, pos):
        if next_pos in visited:
            continue

        visited.add(next_pos)
        path_steps = max(path_steps, dfs(inp, next_pos, end_pos, steps+1, visited))
        visited.remove(next_pos)

    return path_steps


def find_longest_path_steps(inp: List[str], start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> int:
    max_steps = -1
    for next_pos in next_coords(inp, start_pos):
        max_steps = max(max_steps, dfs(inp, next_pos, end_pos, 1, set([next_pos])))
    return max_steps


start_end_positions = find_start_end_positions(inp) 
assert len(start_end_positions) == 2
start_pos, end_pos = start_end_positions

print('Part 1:', find_longest_path_steps(inp, start_pos, end_pos))
