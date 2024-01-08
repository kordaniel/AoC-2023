import sys
sys.path.insert(0, '..')


from typing import List, Tuple, Union

from helpers import filemap


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    ' . . F 7 . '.replace(' ', ''),
    ' . F J | . '.replace(' ', ''),
    ' S J . L 7 '.replace(' ', ''),
    ' | F - - J '.replace(' ', ''),
    ' L J . . . '.replace(' ', '')
] # 8

class Coord:

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __eq__(self, other) -> bool:
        return self.y == other.y and self.x == other.x

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'({self.y}, {self.x})'


def find_starting_pos(inp: List[str]) -> Union[Coord, None]:
    for y, row in enumerate(inp):
        for x, char in enumerate(row):
            if char == 'S':
                return Coord(y, x)

    return None


def find_first_moves(inp: List[str], start_pos: Coord) -> List[Coord]:
    coords = []

    for dy in range(-1, 2):
        if start_pos.y + dy < 0 or start_pos.y + dy >= len(inp):
            continue
        y = start_pos.y + dy

        for dx in range(-1, 2):
            if dy == dx or dy+dx == 0:
                continue
            elif start_pos.x + dx < 0 or start_pos.x + dx >= len(inp[y]):
                continue

            x = start_pos.x + dx
            char = inp[y][x]

            if char == '.':
                continue

            is_valid_move = False
            if dy == 0:
                if char == '-': is_valid_move = True
                elif dx == -1 and char in ('L', 'F'): is_valid_move = True
                elif dx ==  1 and char in ('J', '7'): is_valid_move = True
            elif dx == 0:
                if char == '|': is_valid_move = True
                elif dy == -1 and char in ('7', 'F'): is_valid_move = True
                elif dy ==  1 and char in ('J', 'L'): is_valid_move = True

            if is_valid_move:
                coords.append(Coord(y, x))

    return coords


def get_next_coord(prev: Coord, cur: Coord, pipe: str) -> Coord:
    y, x = None, None

    if pipe == '|':
        y = cur.y-1 if cur.y < prev.y else cur.y+1
        x = cur.x
    elif pipe == '-':
        y = cur.y
        x = cur.x-1 if cur.x < prev.x else cur.x+1
    elif pipe == 'L':
        y = cur.y-1 if cur.y == prev.y else cur.y
        x = cur.x   if cur.y == prev.y else cur.x+1
    elif pipe == 'J':
        y = cur.y-1 if cur.y == prev.y else cur.y
        x = cur.x   if cur.y == prev.y else cur.x-1
    elif pipe == '7':
        y = cur.y+1 if cur.y == prev.y else cur.y
        x = cur.x   if cur.y == prev.y else cur.x-1
    elif pipe == 'F':
        y = cur.y+1 if cur.y == prev.y else cur.y
        x = cur.x   if cur.y == prev.y else cur.x+1

    return Coord(y, x)


def walk_pipe(
        inp: List[str],
        prev_positions: Tuple[Coord, Coord],
        cur_positions: Union[Tuple[Coord, Coord], List[Coord]]
) -> int:
    steps = 1

    while cur_positions[0] != cur_positions[1]:
        steps += 1

        left_prev, right_prev = prev_positions
        left_pos, right_pos   = cur_positions

        pipe_first, pipe_second = inp[left_pos.y][left_pos.x], inp[right_pos.y][right_pos.x]

        prev_positions = cur_positions
        cur_positions = (
            get_next_coord(left_prev, left_pos, pipe_first),
            get_next_coord(right_prev, right_pos, pipe_second)
        )

    return steps


start_position = find_starting_pos(inp)
next_positions = find_first_moves(inp, start_position)

#print('start:', start_position)
#print('first:', next_positions)
steps = walk_pipe(inp, (start_position, start_position), next_positions)

print('Part 1:', steps)
