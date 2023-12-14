import sys
sys.path.insert(0, '..')

from typing import List

from helpers import filemap


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....'
] # 136

class Reflector:

    def __init__(self, inp: List[str]):
        self.__rocks = [list(row) for row in inp]


    def tilt_north(self) -> None:
        for row in range(len(self.__rocks)):
            for col in range(len(self.__rocks[row])):
                if self.__rocks[row][col] != 'O':
                    continue
                self.__roll_rock(row, col, -1)


    def get_north_support_beams_load(self) -> int:
        total = 0
        for i, row in enumerate(self.__rocks):
            total += (len(self.__rocks)-i) * sum([1 for c in row if c == 'O'])
        return total


    def __roll_rock(self, y: int, x: int, yd: int) -> None:
        while yd != 0 and y+yd >= 0 and self.__rocks[y+yd][x] == '.':
            self.__rocks[y+yd][x] = self.__rocks[y][x]
            self.__rocks[y][x] = '.'
            y += yd


    def __str__(self) -> str:
        return '\n'.join([''.join(r) for r in self.__rocks])



r = Reflector(inp)
r.tilt_north()
print(r.get_north_support_beams_load())
