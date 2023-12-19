import enum
import math
from functools import total_ordering
from io        import StringIO
from typing    import Any, Callable, Iterable, List, Tuple


@total_ordering
@enum.unique
class CartesianDir(enum.Enum):
    N  = (-1,  0)
    NE = (-1,  1)
    E  = ( 0,  1)
    SE = ( 1,  1)
    S  = ( 1,  0)
    SW = ( 1, -1)
    W  = ( 0, -1)
    NW = (-1, -1)

    def __hash__(self) -> int:
        return hash(self.value)

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __eq__(self, other) -> bool:
        return self.value == other.value


CARTESIAN_DIRECTIONS = {
    'N':  (-1,  0),
    'NE': (-1,  1),
    'E':  ( 0,  1),
    'SE': ( 1,  1),
    'S':  ( 1,  0),
    'SW': ( 1, -1),
    'W':  ( 0, -1),
    'NW': (-1, -1)
}


class Vec2D:

    def __init__(self, y: int, x: int):
        self.__y = y
        self.__x = x


    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, y: int) -> None:
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int) -> None:
        self.__x = x

    def get_coords(self) -> Tuple[int, int]:
        return (self.y, self.x)

    def get_opposite(self) -> 'Vec2D':
        return Vec2D(-self.y, -self.x)

    def add_tuple(self, rhs: Tuple[int, int]) -> None:
        self.__y += rhs[0]
        self.__x += rhs[1]

    def transform(self, direction: CartesianDir, steps: int = 1) -> None:
        self.__y += steps * direction.value[0]
        self.__x += steps * direction.value[1]

    def __hash__(self) -> int:
        return hash(self.get_coords())

    def __eq__(self, other) -> bool:
        return self.y == other.y and self.x == other.x

    def __add__(self, other) -> 'Vec2D':
        return Vec2D(self.y + other.y, self.x + other.x)

    def _iadd__(self, other) -> None:
        self.__y += other.y
        self.__x += other.x

    def __str__(self) -> str:
        return f'({self.y}, {self.x})'



def filemap(fname: str, func: Callable[[str], Any] = str, sep: str ='\n') -> List[Any]:
    with open(fname, 'r') as f:
        return list(map(func, f.read().strip().split(sep)))


def apply_operator_elementwise(
        binary_operator: Callable[[Any, Any], Any],
        a: Iterable[Any],
        b: Iterable[Any]
) -> Tuple[Any, ...]:
    '''
    Applies the given operator for every pair of elements with matching indexes
    in both of the iterables. Returns the results packed into a new tuple.
    '''
    return tuple(binary_operator(l, r) for l, r in zip(a, b))


def print_matrix(mat: Iterable[Iterable[Any]], spacing: int = 3) -> None:
    print(' r\c |', end='')

    for c in range(len(mat[0])):
        if c < len(mat[0])-1:
            print(f'{c:^{spacing+2}}|', end='')
        else:
            print(f'{c:^{spacing+2}}')
    print('-' * (5 + (spacing+3) * len(mat[0])), sep='')

    for i, l in enumerate(mat):
        print(f'{i:^5}|', end='')
        for char in l[:-1]:
            print(f'{char:^{spacing+2}}|', end='')
        for char in l[-1]:
            print(f'{char:^{spacing+2}}')



def transpose_matrix(mat: Iterable[Iterable[Any]]) -> Tuple[Tuple[Any, ...], ...]:
    return tuple(zip(*mat))


def print_binarytree(
        tree: List[Any],
        total_width: int = 60,
        fill: str = ' '
) -> None:
    output = StringIO()
    last_row = -1

    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i+1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')

        columns = 2**row
        col_width = int(math.floor((total_width*1.0) / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row

    print(output.getvalue())
    print('-' * total_width)
