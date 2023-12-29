import sys
sys.path.insert(0, '..')
sys.setrecursionlimit(8000)


from typing import Dict, List, Set, Tuple

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
] # 154

H, W = len(inp), len(inp[0])


def find_start_end_positions(inp: List[str]) -> List[Tuple[int, int]]:
    start = tuple((0, c) for c in range(W) if inp[0][c] == '.')
    end   = tuple((H-1, c) for c in range(W) if inp[H-1][c] == '.')
    return [*start, *end]


def in_bounds(coords: Tuple[int, int]) -> bool:
    return 0 <= coords[0] < H and 0 <= coords[1] < W


def next_coords(inp: List[str], coords: Tuple[int, int]) -> List[Tuple[int, int]]:
    coords_lst = list()

    for dir in (CartesianDir.N, CartesianDir.E, CartesianDir.S, CartesianDir.W):
        next_pos = coords[0] + dir.value[0], coords[1] + dir.value[1]
        if not in_bounds(next_pos):
            continue
        elif inp[next_pos[0]][next_pos[1]] == '#':
            continue
        coords_lst.append(next_pos)

    return coords_lst


def parse_input(inp: List[str]) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    nodes = dict()
    for y in range(H):
        for x in range(W):
            if inp[y][x] == '#':
                continue
            edges = next_coords(inp, (y, x))
            if len(edges) > 2:
                nodes[(y, x)] = edges

    return nodes

def construct_graph(
        nodes: Dict[Tuple[int, int], List[Tuple[int, int]]],
        end_pos: Tuple[int, int]
) -> Dict[Tuple[int, int], Dict[Tuple[int, int], int]]:
    graph = dict()

    for start_pos, first_positions in nodes.items():
        visited = set([start_pos])
        for initial_step_pos in first_positions:
            visited.add(initial_step_pos)
            path_steps, path_end_pos = dfs_count_path_steps(inp, set(nodes.keys()), visited, initial_step_pos, end_pos, 1)
            visited.remove(initial_step_pos)

            if not start_pos in graph:
                graph[start_pos] = dict()
            if not path_end_pos in graph:
                graph[path_end_pos] = dict()

            graph[start_pos][path_end_pos] = path_steps
            graph[path_end_pos][start_pos] = path_steps

    return graph


def dfs_count_path_steps(
        inp: List[str],
        nodes: Set[Tuple[int, int]], # Intersections, nodes that have over 2 outgoing edges
        visited: Set[Tuple[int, int]],
        pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        depth: int
) -> Tuple[int, Tuple[int, int]]:
    path_info = (depth, pos)

    for next_pos in next_coords(inp, pos):
        if next_pos == end_pos:
            return depth + 1, next_pos
        elif next_pos in visited:
            continue
        elif next_pos in nodes:
            return depth + 1, next_pos

        visited.add(next_pos)

        path_len, path_end_pos = dfs_count_path_steps(inp, nodes, visited, next_pos, end_pos, depth + 1)
        if path_len > path_info[0]:
            path_info = path_len, path_end_pos
        else:
            assert False # Should never encounter any nodes that have several outging edges

        visited.remove(next_pos)

    return path_info


def dfs_steps_in_longest_path(
        graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]],
        visited: Set[Tuple[int, int]],
        pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        steps: int
) -> int:
    total_steps = 0

    for next_pos in graph[pos]:
        if next_pos == end_pos:
            return steps + graph[pos][next_pos]
        elif next_pos in visited:
            continue

        visited.add(next_pos)

        path_steps = dfs_steps_in_longest_path(graph, visited, next_pos, end_pos, steps + graph[pos][next_pos])

        if path_steps > total_steps:
            total_steps = path_steps

        visited.remove(next_pos)

    return total_steps


start_pos, end_pos = find_start_end_positions(inp) 
nodes_edges = parse_input(inp)
nodes_edges[start_pos] = next_coords(inp, start_pos)
graph = construct_graph(nodes_edges, end_pos)

print('Part 2:', dfs_steps_in_longest_path(graph, set(), start_pos, end_pos, 0))
