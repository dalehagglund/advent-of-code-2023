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

def solve1(sections: list[list[str]], shift) -> int:
    space = Universe.from_lines(sections[0])
    space.expand(scale=shift)

    galaxies = space.galaxy_positions()
    total = 0
    for pos1, pos2 in itertools.combinations(galaxies, 2):
        total += pos1.manhattan_dist(pos2)
    return total
        
def solve2(sections: list[list[str]]) -> int:
    pass
    
def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***', solve1(sections, shift=2))
    
def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve1(sections, shift=1000000))

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
