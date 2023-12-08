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
)
import numpy as np
from pprint import pprint

from tools import *

def parse_input(sections):
    directions = itertools.cycle(sections[0][0])
    
    s = iter(sections[1])
    s = map(partial(re.split, "[ =(),]+"), s)
    network = {
        node: (left, right)
        for node, left, right, _
        in s
    }

    return directions, network

def follow(net, dirs, start, final):
    print(f'{start = }')
    steps = 0
    node = start
    while not final(node):
        steps += 1
        dir = next(dirs)
        node = net[node]["LR".index(dir)]
    print(f'final = {node}')

    return steps
    
def solve1(sections) -> int:
    directions, network = parse_input(sections)
    
    s = iter(sections[1])
    s = map(partial(re.split, "[ =(),]+"), s)
    network = {
        node: (left, right)
        for node, left, right, _
        in s
    }
    
    return follow(
        network, directions,
        'AAA',
        lambda n: n == 'ZZZ'
    )
    
def solve2(sections) -> int:
    import math
    directions, network = parse_input(sections)
    
    def initial(n: str): return n.endswith('A')
    def final(n: str): return n.endswith('Z')
    
    nodes = [ n for n in network.keys() if initial(n) ]
    steps = [ 
        follow(network, directions, n, final)
        for n
        in nodes
    ]
    print(steps)
    return math.lcm(*steps)

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***', solve1(sections))
    
def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve2(sections))

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
