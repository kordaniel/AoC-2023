import sys
sys.path.insert(0, '..')

from helpers import filemap
from functools import reduce


inp = filemap('input.txt')
inp = [g.split(': ') for g in inp]
inp = [(int(g[0].split(' ')[1]), g[1].split('; ')) for g in inp]
inp = [g[1] for g in inp]

cubes_set_min_power_sum = 0
for game in inp:
    min_cubes = {}
    for cubes in game:
        for cubecols in cubes.split(', '):
            cnt, col = cubecols.split(' ')
            if not col in min_cubes or int(cnt) > min_cubes[col]:
                min_cubes[col] = int(cnt)
    cubes_set_min_power_sum += reduce(lambda c, tot: c*tot, min_cubes.values(), 1)

print(cubes_set_min_power_sum)

