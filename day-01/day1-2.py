import re
from typing import List

str_to_int = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def read_inp() -> List[str]:
    with open('input.txt', 'r') as inp:
        return inp.readlines()

pattern = re.compile(r'([1-9]|one|two|three|four|five|six|seven|eight|nine)')
lines_sum = 0

for l in read_inp():
    line_nums = []
    match = pattern.search(l)
    while match:
        line_nums.append(match[0])
        match = pattern.search(l, match.end() if len(match[0]) == 1 else match.end()-1)

    num = ''.join(map(lambda s: s if s.isdigit() else str_to_int[s], (line_nums[0], line_nums[-1])))
    lines_sum += int(num)

print(lines_sum)

