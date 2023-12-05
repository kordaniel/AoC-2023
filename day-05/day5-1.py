import sys
sys.path.insert(0, '..')

from helpers import filemap
from typing import List, Tuple, Dict


use_test_data = False
inp = filemap('input.txt', sep='\n\n') if not use_test_data else [
    'seeds: 79 14 55 13',
    '''seed-to-soil map:
50 98 2
52 50 48''',
    '''soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15''',
    '''fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4''',
    '''water-to-light map:
88 18 7
18 25 70''',
    '''light-to-temperature map:
45 77 23
81 45 19
68 64 13''',
    '''temperature-to-humidity map:
0 69 1
1 0 69''',
    '''humidity-to-location map:
60 56 37
56 93 4'''
] # 13 -> 35


map_types = []
seeds = [int(seed) for seed in inp[0].split(': ')[1].split()]
maps = {}


for m in inp[1:]:
    lines = m.split('\n')

    map_types.append(lines[0].split()[0])
    maplist = [tuple(map(int, v.split())) for v in lines[1:]]
    maps[lines[0].split()[0]] = maplist


def get_mapping(mappings: Dict[str, List[Tuple[int, int, int]]], map_type: str, i: int) -> int:
    maplists = mappings[map_type]

    for mappings in maplists:
        dest, source, range = mappings
        if source <= i < source + range:
            return dest + i - source

    return i


def get_location(
    mappings: Dict[str, List[Tuple[int, int, int]]],
    map_types: List[str],
    seed: int
) -> Tuple[int, int]:
    source_dest = get_mapping(mappings, map_types[0], seed)
    for t in map_types[1:]:
        source_dest = get_mapping(mappings, t, source_dest)
    return seed, source_dest


def find_lowest_location(
        seeds: List[int],
        mappings: Dict[str, List[Tuple[int, int, int]]],
        map_types: List[str]
) -> Tuple[int, int]:
    min_loc, min_seed = 10**10, None

    for seed in seeds:
        soil, loc = get_location(mappings, map_types, seed)
        if loc < min_loc:
            min_loc = loc
            min_seed = soil

    return min_seed, min_loc


print(' -> '.join(map(str, find_lowest_location(seeds, maps, map_types))))
