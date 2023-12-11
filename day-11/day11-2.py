import sys
sys.path.insert(0, '..')

from typing import List, Tuple
import itertools
import operator

from helpers import filemap, apply_operator_elementwise, transpose_matrix

EXPANSION_SIZE = 10**6

use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    ' . . . # . . . . . . '.replace(' ', ''),
    ' . . . . . . . # . . '.replace(' ', ''),
    ' # . . . . . . . . . '.replace(' ', ''),
    ' . . . . . . . . . . '.replace(' ', ''),
    ' . . . . . . # . . . '.replace(' ', ''),
    ' . # . . . . . . . . '.replace(' ', ''),
    ' . . . . . . . . . # '.replace(' ', ''),
    ' . . . . . . . . . . '.replace(' ', ''),
    ' . . . . . . . # . . '.replace(' ', ''),
    ' # . . . # . . . . . '.replace(' ', '')
] # 82000210


class Galaxy:

    def __init__(self, id: int, coords: Tuple[int, int]):
        self.__id = id
        self.__coords = coords

    @property
    def id(self) -> int:
        return self.__id

    @property
    def coords(self) -> Tuple[int, int]:
        return self.__coords


    def __repr__(self) -> str:
        return f'{self.id:2} {self.coords}'


    def __str__(self) -> str:
        return self.__repr__()



def get_empty_rows(inp: List[str]) -> Tuple[int, ...]:
    return tuple(r for r, row in enumerate(inp) if all(c == '.' for c in row))


def get_empty_cols(inp: List[str]) -> Tuple[int, ...]:
    return get_empty_rows(transpose_matrix(inp))


def parse_input(inp: List[str]) -> List[Galaxy]:
    galaxies = []
    empty_rows = get_empty_rows(inp)
    empty_cols = get_empty_cols(inp)

    galaxy_n = 1
    yi = -1
    dy = 0

    for y, l in enumerate(inp):
        while len(empty_rows) > 0 and yi < len(empty_rows)-1 and empty_rows[yi+1] < y:
            dy += (EXPANSION_SIZE-1)
            yi += 1

        xi = -1
        dx = 0

        for x, c in enumerate(l):
            while len(empty_cols) > 0 and xi < len(empty_cols)-1 and empty_cols[xi+1] < x:
                dx += (EXPANSION_SIZE-1)
                xi += 1

            if c == '#':
                galaxies.append(Galaxy(galaxy_n, (y+dy,  x+dx)))
                galaxy_n += 1

    return galaxies


def manhattan_dist(a: Galaxy, b: Galaxy) -> int:
    return sum(abs(d) for d in apply_operator_elementwise(operator.sub, a.coords, b.coords))


def get_distances(galaxies: List[Galaxy]) -> Tuple[Tuple[str, int], ...]:
    combinations = itertools.combinations(galaxies, 2)
    return tuple((f'{p[0].id}<->{p[1].id}', manhattan_dist(p[0], p[1])) for p in combinations)


galaxies = parse_input(inp)
distances = get_distances(galaxies)

print(sum(d[1] for d in distances))
