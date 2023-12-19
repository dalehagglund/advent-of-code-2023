import sys
import typing as ty
from dataclasses import dataclass, field
from enum import Enum
import collections
import re
import itertools
from itertools import (
    islice,
    pairwise,
    zip_longest
)
from functools import (
    partial,
    reduce,
    lru_cache,
)
import numpy as np
from pprint import pprint
import contextlib
import time
import operator

from tools import *
from work import *

def check_is_tree(flowset: dict[str, Flow]) -> bool:
    root = 'in'
    c = collections.Counter()
    
    for name, flow in flowset.items():
        c.update(flow.out() - { "A", "R" })
        
    assert c[root] == 0
    ckeys = set(c.keys())
    fkeys = set(flowset.keys()) - { "in" }
    assert ckeys == fkeys
    assert all(count == 1 for key, count in c.items())

def solve1(sections: list[list[str]]) -> int:
    return -1

def solve2(sections: list[list[str]]) -> int:
    return -1

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    
    s = iter(sections[0])
    s = map(Flow.from_str, s)    
    workflows = dict(
        (flow.name(), flow)
        for flow
        in s
    )
    assert 'in' in workflows
    check_is_tree(workflows)
    
    s = sections[1]
    parts = list(map(Part.from_str, s))
    
    total = 0
    for part in parts:
        flowname = 'in'
        while flowname not in ('R', 'A'):
            flowname = workflows[flowname].eval(part)
        if flowname == "A":
            total += part.x + part.m + part.a + part.s
        
    print(f'*** part 1 ***', total)
    
def count_accepted(flowset, flow, pos, parts, depth=0) -> int:
    recur = partial(count_accepted, flowset, depth=depth+1)

    prefix = " " * (depth * 2)
    print(f'ca> {prefix}{(flow.name(), pos, parts) = }')

    if parts.size() == 0:
        return 0

    rule = flow[pos]
    out = rule.out()
    
    if pos == len(rules) - 1 and out == "A":
        return parts.size()
    elif pos == len(rules) - 1 and out == "R":
        return 0
    elif pos == len(rules) - 1:
        return recur(flowset[out], 0, parts)
        
    assert pos + 1 < len(rules)

    trueparts, falseparts = rule.split_range(parts)    
    if out == "A":
        return (
            trueparts.size() + 
            recur(rules,        pos + 1, falseparts)
        )
    elif out == "R":
        return (
            recur(rules,        pos + 1, falseparts)
        )
    else:
        return (
            recur(rules,        pos + 1, falseparts) +
            recur(flowset[out],       0, trueparts)
        )

    assert False, "shouldn't get here"

def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve2(sections))

def usage(message):
    prog = sys.argv[0]
    print(f'usage: {prog} [-1|-2] [--] input_file...')
    print(f'    {message}')
    sys.exit(1)

def main(args):
    infile = None
    run1 = run2 = False
    
    while args and args[0].startswith('-'):
        arg = args.pop(0)
        if arg in ('--'): break
        elif re.match(r'^-[A-Za-z0-9]{2,}$', arg):
            args[:0] = list(map(partial(operator.add, '-'), arg[1:]))
        elif arg in ('-1'): run1 = True
        elif arg in ('-2'): run2 = True
        else:
            usage(f'{arg}: unexpected option')

    if not (run1 or run2): run1 = run2 = True

    if len(args) == 0:
        usage("missing input file")
        
    if run1:
        for infile in args:
            part1(infile)

    if run2:
        for infile in args:
            part2(infile)
    
if __name__ == '__main__':
    main(sys.argv[1:])
