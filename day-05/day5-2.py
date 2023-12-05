import sys
sys.path.insert(0, '..')

from helpers import filemap
from typing import Tuple


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
] # 82 -> 46


map_types = []
maps = {}
seeds_list = [int(seed) for seed in inp[0].split(': ')[1].split()]
seeds = [] # [start, end)

for i in range(0, len(seeds_list), 2):
    seeds.append((seeds_list[i], seeds_list[i] + seeds_list[i+1]))

seeds = sorted(seeds)


for m in inp[1:]:
    lines = m.split('\n')

    map_types.append(lines[0].split()[0])
    maplist = [tuple(map(int, v.split())) for v in lines[1:]]
    maps[lines[0].split()[0]] = maplist


def is_valid_seed(seed: int) -> bool:
    for s in seeds:
        if s[0] <= seed < s[1]:
            return True
    return False


def get_source(destination: int, map_type: str) -> int:
    maplists = maps[map_type]

    for mapping in maplists:
        dest, source, map_range = mapping
        if dest <= destination < dest + map_range:
            return source + (destination - dest)

    return destination


def find_lowest_location() -> Tuple[int, int]:
    location = 0
    soil = None
    map_types_inv = list(reversed(map_types))

    while True:
        #if location % 100000 == 0:
        #    print(location)
        src_dst = location

        for map_type in map_types_inv:
            src_dst = get_source(src_dst, map_type)

        if is_valid_seed(src_dst):
            soil = src_dst
            break
        else:
            location += 1

    return soil, location

# Brute-force solution, runtime is LONG
print(' -> '.join(map(str, find_lowest_location())))
