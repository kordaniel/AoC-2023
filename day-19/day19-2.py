import sys
sys.path.insert(0, '..')

import re
import math

from typing import Dict, List, Tuple, Union

from helpers import filemap


use_test_data = False
inp = filemap('input.txt', lambda p: p.split('\n'), sep='\n\n') if not use_test_data else [
    [
        'px{a<2006:qkq,m>2090:A,rfg}',
        'pv{a>1716:R,A}',
        'lnx{m>1548:A,A}',
        'rfg{s<537:gd,x>2440:R,A}',
        'qs{s>3448:A,lnx}',
        'qkq{x<1416:A,crn}',
        'crn{x>2662:A,R}',
        'in{s<1351:px,qqz}',
        'qqz{s>2770:qs,m<1801:hdj,R}',
        'gd{a>3333:R,R}',
        'hdj{m>838:A,pv}'
    ],
    [
        '{x=787,m=2655,a=1222,s=2876}',
        '{x=1679,m=44,a=2067,s=496}',
        '{x=2036,m=264,a=79,s=2244}',
        '{x=2461,m=1339,a=466,s=291}',
        '{x=2127,m=1623,a=2188,s=1013}'
    ]
] # 167409079868000


def parse_workflows(workflows: List[str]) -> Dict[str, List[Union[Tuple[str], Tuple[str, str, int, str]]]]:
    rules = dict()

    for wf in workflows:
        i = wf.index('{')
        name = wf[:i]
        rules[name] = []
        for rule in wf[i+1:-1].split(','):
            colon_i = rule.find(':')
            if colon_i == -1:
                rules[name].append((rule, ))
            else:
                r = rule[:colon_i]
                dst = rule[colon_i+1:]
                op_i = re.search(r'>|<|=', r).start()
                part, val = r.split(r[op_i:op_i+1])
                rules[name].append((part, r[op_i], int(val), dst)) # part.field, operator, comparison val, dest_workflow

    return rules


def count_accepted_ratings(
        workflow: Dict[str, List[Union[Tuple[str], Tuple[str, str, int, str]]]],
        dest: str,
        ratings: Dict[str, Tuple[int, int]],
        depth: int
):
    ct = 0

    for rule in workflow[dest]:
        if len(rule) == 1:
            if rule[0] == 'A':
                ct += math.prod(v[1]-v[0]+1 for v in ratings.values())
            elif rule[0] != 'R':
                ct += count_accepted_ratings(workflow, rule[0], ratings, depth+1)
            break

        left = ratings[rule[0]]

        if rule[1] == '<':
            if left[0] >= rule[2]:
                continue

            ratings_next = ratings.copy()

            if left[1] >= rule[2]:
                next = (left[0], rule[2]-1)
                ratings[rule[0]] = (rule[2], left[1])
            else: # if true => crash at next leaf
                next = left
                ratings[rule[0]] = (None, None)

            ratings_next[rule[0]] = next

            if rule[3] == 'A':
                ct += math.prod(v[1]-v[0]+1 for v in ratings_next.values())
            elif rule[3] == 'R':
                continue
            else:
                ct += count_accepted_ratings(workflow, rule[3], ratings_next, depth+1)

        elif rule[1] == '>':
            if left[1] <= rule[2]:
                continue

            ratings_next = ratings.copy()

            if left[0] <= rule[2]:
                next = (rule[2]+1, left[1])
                ratings[rule[0]] = (left[0], rule[2])
            else: # if true => crash at next leaf
                next = left
                ratings[rule[0]] = (None, None)

            ratings_next[rule[0]] = next

            if rule[3] == 'A':
                ct += math.prod(v[1]-v[0]+1 for v in ratings_next.values())
            elif rule[3] == 'R':
                continue
            else:
                ct += count_accepted_ratings(workflow, rule[3], ratings_next, depth+1)
        else:
            assert False

    return ct


wflows = parse_workflows(inp[0])

c = count_accepted_ratings(
    wflows,
    'in',
    { 'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000) }
    ,
    0
)

print('Part 2:', c)
