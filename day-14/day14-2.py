import sys
sys.path.insert(0, '..')

from typing import List

from helpers import filemap, CARTESIAN_DIRECTIONS


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
] # 64

class Reflector:
    '''
    Solves Part 2 in a few seconds => Totally unoptimized implementation, for example
    walks the 2d arr in roworder and updates every index at every iteration.
    '''

    def __init__(self, inp: List[str]):
        self.__rocks = [list(row) for row in inp]


    def tilt(self, y_dir: int, x_dir: int) -> None:
        if y_dir != 0:
            for row in (range(len(self.__rocks)) if y_dir < 0 else range(len(self.__rocks)-1, -1, -1)):
                for col in range(len(self.__rocks[row])):
                    if self.__rocks[row][col] != 'O':
                        continue
                    self.__roll_rock_vertical(row, col, y_dir)

        if x_dir != 0:
            for col in (range(len(self.__rocks[0])) if x_dir < 0 else range(len(self.__rocks[0])-1, -1, -1)):
                for row in range(len(self.__rocks)):
                    if self.__rocks[row][col] != 'O':
                        continue
                    self.__roll_rock_horizontal(row, col, x_dir)


    def spin_cycle(self) -> None:
        for dir in (CARTESIAN_DIRECTIONS[d] for d in tuple('NWSE')):
            self.tilt(*dir)


    def run_cycles(self, n: int) -> None:
        cycles = 0
        counter = dict()

        counter[self.__hash__()] = cycles # No collissions in the input => works
        self.spin_cycle()
        cycles += 1

        while cycles < n and self.__hash__() not in counter:
            counter[self.__hash__()] = cycles
            self.spin_cycle()
            cycles += 1

        if cycles == n:
            return cycles

        initial_len = counter[self.__hash__()]
        loop_len = cycles-initial_len

        cycles_cnt = (n-initial_len) // loop_len
        total_cycles = initial_len + cycles_cnt * loop_len

        while total_cycles < n:
            self.spin_cycle()
            total_cycles += 1


    def get_north_support_beams_load(self) -> int:
        total = 0
        for i, row in enumerate(self.__rocks):
            total += (len(self.__rocks)-i) * sum([1 for c in row if c == 'O'])
        return total


    def __roll_rock_vertical(self, y: int, x: int, yd: int) -> None:
        while yd != 0 and 0 <= y+yd < len(self.__rocks) and self.__rocks[y+yd][x] == '.':
            self.__rocks[y+yd][x] = self.__rocks[y][x]
            self.__rocks[y][x] = '.'
            y += yd


    def __roll_rock_horizontal(self, y: int, x: int, xd: int) -> None:
        while xd != 0 and 0 <= x+xd < len(self.__rocks[y]) and self.__rocks[y][x+xd] == '.':
            self.__rocks[y][x+xd] = self.__rocks[y][x]
            self.__rocks[y][x] = '.'
            x += xd


    def __hash__(self) -> int:
        return hash(tuple(tuple(r) for r in self.__rocks))


    def __str__(self) -> str:
        return '\n'.join([''.join(r) for r in self.__rocks])



CYCLES = 1000000000

r = Reflector(inp)
r.run_cycles(CYCLES)
print(r.get_north_support_beams_load())
