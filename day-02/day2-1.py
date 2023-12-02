import sys
sys.path.insert(0, '..')

from helpers import filemap

cubes_cnt = {
    'red': 12,
    'green': 13,
    'blue': 14
}

inp = filemap('input.txt')
inp = [g.split(': ') for g in inp]
inp = [(int(g[0].split(' ')[1]), g[1].split('; ')) for g in inp]

#for l in inp[:3]: print (l)

inp = [(g[0], [cube.split(', ') for cube in g[1]]) for g in inp]

id_sum = 0
for g_id, subset in inp:
    possible = True
    for cubes in subset:
        for c in cubes:
            cnt, col = c.split(' ')
            if int(cnt) > cubes_cnt[col]:
                possible = False
                break
        if not possible:
            break
    if possible:
        id_sum += g_id

print(id_sum)

