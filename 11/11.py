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
from spacetime import *

def find_galaxies(space: Universe) -> list[Point]:
    return [
        Point(r, c)
        for (r, c) in product(space.nrow(), space.ncol())
        if space.at((r,c)) == '#'
    ]
    
def solve1(sections: list[list[str]]) -> int:
    space = Universe.from_lines(sections[0])
    space.expand_empty_rows()
    space.expand_empty_cols()
    pprint(space)

    galaxies = find_galaxies(space)
    for i, point in enumerate(sorted(galaxies)):
        print(f'   {i:2d}: {point}')

    for i, pos in enumerate(galaxies):
        print(f'   {i:2d} {Point(0, 4).manhattan_dist(pos) = }')

    total = 0
    for pos1, pos2 in itertools.combinations(galaxies, 2):
        total += pos1.manhattan_dist(pos2)
    return total
        
def solve2(sections: list[list[str]]) -> int:
    pass
    
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
