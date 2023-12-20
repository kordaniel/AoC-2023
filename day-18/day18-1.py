import sys
sys.path.insert(0, '..')

from collections import deque
import operator

from typing import List, Set, Tuple

from helpers import filemap, CartesianDir, apply_operator_elementwise


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)'
] # 62


def parse_input(inp: List[str]) -> List[Tuple[str, int, str]]:
    lines = []
    for li in inp:
        l = li.split()
        lines.append((l[0], int(l[1]), l[2][2:-1]))
    return lines


def bfs(
        visited: Set[Tuple[int, int]],
        start_pos: Tuple[int, int],
        T: int,
        B: int,
        L: int,
        R: int
) -> Set[Tuple[Set[Tuple[int, int]], int]]:

    q = deque([start_pos])
    visited_count = 0

    while len(q) > 0:
        pos = q.popleft()
        if pos in visited:
            continue

        visited.add(pos)
        visited_count += 1

        for dir in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            next = apply_operator_elementwise(operator.add, pos, dir)
            if next[0] < T or next[0] > B or next[1] < L or next[1] > R:
                continue

            q.append(next)

    return visited, visited_count


def dig(dig_plan: List[Tuple[str, int, str]]):
    path = [(0, 0)]
    visited = set(path)

    T, B = 0, 0
    L, R = 0, 0

    for l in dig_plan:
        if l[0] == 'R':
            dir = CartesianDir.E.value
        elif l[0] == 'D':
            dir = CartesianDir.S.value
        elif l[0] == 'L':
            dir = CartesianDir.W.value
        elif l[0] == 'U':
            dir = CartesianDir.N.value
        else:
            assert False

        for _ in range(l[1]):
            prev = path[-1]
            next = apply_operator_elementwise(operator.add, prev, dir)
            path.append(next)
            visited.add(next)
            T = min(T, next[0])
            B = max(B, next[0])
            L = min(L, next[1])
            R = max(R, next[1])

    ground_count = 0

    for r in (T, B):
        for c in range(L, R+1):
            if (r, c) in visited:
                continue
            iter_visited, c = bfs(visited, (r, c), T, B, L, R)
            visited.union(iter_visited)
            ground_count += c
    for r in range(T, B+1):
        for c in (L, R):
            if (r, c) in visited:
                continue
            iter_visited, c = bfs(visited, (r, c), T, B, L, R)
            visited.union(iter_visited)
            ground_count += c

    return (B-T+1)*(R-L+1)-ground_count


inp = parse_input(inp)

print('Lagoon size:', dig(inp))
