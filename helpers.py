from typing import Any, Callable, Iterable, List, Tuple


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
