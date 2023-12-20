import sys
sys.path.insert(0, '..')

from typing import List, Tuple, Union

from helpers import filemap


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
] # 952408144115


def parse_input(inp: List[str]) -> List[Tuple[str, int]]:
    dirmap = dict(zip(tuple('0123'), tuple('RDLU')))
    lines = []
    for li in inp:
        l = li.split()
        lines.append((dirmap[l[2][-2]], int(l[2][2:7], 16)))
    return lines


def det(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return a[0]*b[1] - a[1]*b[0]


def dig(dig_plan: List[Tuple[str, int]]) -> Union[int, float]:
    prev = (0, 0)
    lines_hor = []
    lines_ver = []
    vertices = []

    T, B = 0, 0
    L, R = 0, 0

    for l in dig_plan:
        distance = l[1]
        if l[0] == 'R':
            vertex = (prev[0], prev[1] + distance)
            lines_hor.append((prev, vertex))
        elif l[0] == 'D':
            vertex = (prev[0] + distance, prev[1])
            lines_ver.append((prev, vertex))
        elif l[0] == 'L':
            vertex = (prev[0], prev[1] - distance)
            lines_hor.append((vertex, prev))
        elif l[0] == 'U':
            vertex = (prev[0] - distance, prev[1])
            lines_ver.append((vertex, prev))
        else:
            assert False

        vertices.append(vertex)
        prev = vertex
        T = min(T, prev[0])
        B = max(B, prev[0])
        L = min(L, prev[1])
        R = max(R, prev[1])

    polygon_area = sum(det(vertices[i], vertices[(i+1) % len(vertices)]) for i in range(len(vertices))) / 2
    vertical_lines_area   = sum(abs(l[1][0]-l[0][0]) for l in lines_ver) / 2
    horizontal_lines_area = sum(abs(l[1][1]-l[0][1]) for l in lines_hor) / 2

    # Need to add one to the total area, since we are only accounting for half of the "width" of the
    # edge lines areas, which only accounts for 1/4 of the area at every vertex that are "turning clockwise"
    # and in a closed loop there are always 4 more of those than edges turning counter clockwise.
    total_area = abs(polygon_area) + vertical_lines_area + horizontal_lines_area + 1

    if total_area.is_integer():
        return int(total_area)
    return total_area


inp = parse_input(inp)

print('Lagoon size:', dig(inp))
