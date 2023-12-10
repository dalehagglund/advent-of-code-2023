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
from grid import *

def find_max_depth(graph, start):

    max_depth = float('-inf')
    seen = set()
    queue = collections.deque()
    queue.append((start, 0))
    while len(queue) > 0:
        label, depth = queue.popleft()
        if label in seen:
            continue
        seen.add(label)
        max_depth = max(max_depth, depth)
        queue.extend(
            (neighbour, depth + 1)
            for neighbour
            in graph.neighbours(label)
        )
        
    return max_depth
            
   

def solve1(sections: list[list[str]]) -> int:
    grid = Grid.from_map(sections[0])
    pprint(grid)
    return find_max_depth(grid, grid.start())

def solve2(sections: list[list[str]]) -> int:
    return -1

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
