import sys
sys.path.insert(0, '..')

from helpers import filemap


use_test_data = False
inp = filemap('input.txt', sep=',') if not use_test_data else [
    'rn=1',
    'cm-',
    'qp=3',
    'cm=2',
    'qp-',
    'pc=4',
    'ot=9',
    'ab=5',
    'pc-',
    'pc=6',
    'ot=7'
] # 145


class Box:

    def __init__(self):
        self.__lenses = list()
        self.__lenses_positions = dict()


    @property
    def length(self) -> int:
        return len(self.__lenses_positions)


    def insert_lens(self, label: str, focal_length: int) -> None:
        i = self.__lenses_positions.get(label, -1)

        if i > -1:
            self.__lenses[self.__lenses_positions[label]] = focal_length
        else:
            j = len(self.__lenses)
            self.__lenses.append(focal_length)
            self.__lenses_positions[label] = j


    def remove_lens(self, label: str) -> None:
        i = self.__lenses_positions.get(label, -1)
        if i == -1:
            return
        self.__lenses[i] = None
        del self.__lenses_positions[label]


    def get_focusing_power(self) -> int:
        p = 0
        i = 0
        for l in self.__lenses:
            if l is None:
                continue
            i += 1
            p += i * l
        return p


    def __repr__(self) -> str:
        position_label = dict([tuple(reversed(p)) for p in self.__lenses_positions.items()])
        return ' '.join(f'[{position_label[i]} {str(fl)}]' for i, fl in enumerate(self.__lenses) if fl is not None)


    def __str__(self) -> str:
        return self.__repr__()



def compute_hash(inp_string: str) -> int:
    result = 0
    for c in (ord(c) for c in inp_string):
        result += c
        result *= 17
        result %= 256
    return result


BOXES = tuple(Box() for _ in range(256))

for step in inp:
    if step[-1] == '-':
        label = step[:-1]
        BOXES[compute_hash(label)].remove_lens(label)
    elif (i := step.find('=')):
        label, focal_length = step[:i], int(step[i+1:])
        BOXES[compute_hash(label)].insert_lens(label, focal_length)
    else:
        print('Misformed input line')

#for i, b in enumerate(BOXES, 1):
#    if b.length > 0:
#        print('Box', i-1, b)

lens_configuration_focusing_power = sum(i*b.get_focusing_power() for i, b in enumerate(BOXES, 1))
print(lens_configuration_focusing_power)
