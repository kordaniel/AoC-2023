from typing import Any, Callable, Iterable, List, Tuple


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


def print_matrix(mat: Iterable[Iterable[Any]]) -> None:
    for l in mat:
        print(l)


def transpose_matrix(mat: Iterable[Iterable[Any]]) -> Tuple[Tuple[Any, ...], ...]:
    return tuple(zip(*mat))
