import sys
sys.path.insert(0, '..')

import string
from typing import List, Tuple, Union

from helpers import filemap


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    '1,0,1~1,2,1',
    '0,0,2~2,0,2',
    '0,2,3~2,2,3',
    '0,0,4~0,2,4',
    '2,0,5~2,2,5',
    '0,1,6~2,1,6',
    '1,1,8~1,1,9'
] # 5


class Brick:

    def __init__(self, point_a: Tuple[int, int, int], point_b: Tuple[int, int, int], name: Union[str, int]) -> None:
        self.__name = name
        self.__pnt_a = point_a
        self.__pnt_b = point_b

    @property
    def name(self) -> Union[str, int]:
        return self.__name

    @property
    def max_x(self) -> int:
        return self.__get_val(0, True)

    @property
    def min_x(self) -> int:
        return self.__get_val(0, False)
    
    @property
    def max_y(self) -> int:
        return self.__get_val(1, True)

    @property
    def min_y(self) -> int:
        return self.__get_val(1, False)

    @property
    def max_z(self) -> int:
        return self.__get_val(2, True)

    @property
    def min_z(self) -> int:
        return self.__get_val(2, False)

    @property
    def height(self) -> int:
        return 1 + self.max_z - self.min_z

    def get_descended(self, min_z: int) -> 'Brick':
        if self.__pnt_a[2] <= self.__pnt_b[2]:
            pnt_a = (self.__pnt_a[0], self.__pnt_a[1], min_z)
            pnt_b = (self.__pnt_b[0], self.__pnt_b[1], pnt_a[2] + self.height - 1)
        else:
            pnt_b = (self.__pnt_b[0], self.__pnt_b[1], min_z)
            pnt_a = (self.__pnt_a[0], self.__pnt_a[1], pnt_b[2] + self.height - 1)
        return Brick(pnt_a, pnt_b, self.name)

    def __lt__(self, other: 'Brick') -> bool:
        return self.min_z < other.min_z

    def __get_val(self, idx: int, larger: bool) -> int:
        return self.__pnt_a[idx] if self.__pnt_a[idx] >= self.__pnt_b[idx] else self.__pnt_b[idx] \
            if larger else \
                self.__pnt_a[idx] if self.__pnt_a[idx] <= self.__pnt_b[idx] else self.__pnt_b[idx]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'{self.name}: {self.__pnt_a}-{self.__pnt_b}'


def parse_input(inp: List[str]) -> List[Brick]:
    lines = [[tuple(int(v) for v in tpl.split(',')) for tpl in l.split('~')] for l in inp]
    return [Brick(tpl[0], tpl[1], string.ascii_uppercase[i] if use_test_data else i) for i, tpl in enumerate(lines)]


def descend_bricks(bricks: List[Brick]) -> List[Brick]:
    descended_bricks = list()
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0

    for b in bricks:
        min_x = min(min_x, b.min_x)
        max_x = max(max_x, b.max_x)
        min_y = min(min_y, b.min_y)
        max_y = max(max_y, b.max_y)
    assert min_x >= 0
    assert min_y >= 0
    assert max_x > min_x
    assert max_y > min_y

    xy_heights = [[0] * (max_y+1) for _ in range(max_x+1)]

    for b in sorted(bricks):
        z = 0
        for x in range(b.min_x, b.max_x+1):
            for y in range(b.min_y, b.max_y+1):
                z = max(z, xy_heights[x][y])

        descended_brick = b.get_descended(z+1)
        descended_bricks.append(descended_brick)

        for x in range(descended_brick.min_x, descended_brick.max_x+1):
            for y in range(descended_brick.min_y, descended_brick.max_y+1):
                xy_heights[x][y] = descended_brick.max_z

    #for x in range(len(xy_heights)):
    #    for y in range(len(xy_heights[y])):
    #        print(xy_heights[x][y], end=' ')
    #    print()

    return descended_bricks


def count_disintegretables(bricks: List[Brick]) -> int:
    disintegreteables = set()
    brick_supports = dict()     # brick -> List of bricks that is supported by the brick
    supported_by_brick = dict() # brick -> List of bricks supporting the brick

    for i in range(len(bricks)):
        brick_lower = bricks[i]
        if not brick_lower.name in brick_supports:
            brick_supports[brick_lower.name] = list()

        for j in range(i+1, len(bricks)):
            brick_upper = bricks[j]
            if brick_lower.max_z + 1 != brick_upper.min_z:
                continue
            support_found = False
            for x in range(brick_lower.min_x, brick_lower.max_x+1):
                for y in range(brick_lower.min_y, brick_lower.max_y+1):
                    if brick_upper.min_x <= x <= brick_upper.max_x and brick_upper.min_y <= y <= brick_upper.max_y:
                        if not brick_upper.name in supported_by_brick:
                            supported_by_brick[brick_upper.name] = list()

                        brick_supports[brick_lower.name].append(brick_upper.name)
                        supported_by_brick[brick_upper.name].append(brick_lower.name)
                        support_found = True
                        break
                if support_found:
                    break

    for supporting, supported in brick_supports.items():
        if len(supported) == 0:
            disintegreteables.add(supporting)
            continue

        is_disintegretable = True
        for brick in supported:
            if len(supported_by_brick[brick]) < 2:
                is_disintegretable = False
                break

        if is_disintegretable:
            disintegreteables.add(supporting)

    return len(disintegreteables)


bricks = parse_input(inp)
descended_bricks = descend_bricks(bricks)
print('Part 1:', count_disintegretables(descended_bricks))
