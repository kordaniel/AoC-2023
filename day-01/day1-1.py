import re
from typing import List

def read_inp() -> List[str]:
    with open('input.txt', 'r') as inp:
        return inp.readlines()

lines_sum = 0
for l in read_inp():
    line_nums = re.findall(r'\d', l)
    lines_sum += 10 * int(line_nums[0])
    lines_sum += int(line_nums[-1])

print(lines_sum)

