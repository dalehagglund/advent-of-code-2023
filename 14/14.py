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

def slide_north(grid, col):
    nrow, ncol = len(grid), len(grid[0])
    
    def at(r): return grid[r][col]
    def setpos(r, val): grid[r][col] = val
    
    def span_to_rock(start) -> tuple[int, int, int]:
        ocount = dotcount = 0
        r = start
        while r < nrow and at(r) != "#":
            if at(r) == ".":
                dotcount += 1
            else:
                ocount += 1
            r += 1
        return (r, dotcount, ocount)
        
    def span_rocks(start) -> int:
        if start == nrow: return start
        while start < nrow and at(start) == '#':
            start += 1
        return start
        
    start = 0
    while start < nrow:
        rockpos, ndots, nfloats = span_to_rock(start)
        for r, char in zip(range(start, rockpos), "O" * nfloats + "." * ndots):
            setpos(r, char)
        start = span_rocks(rockpos)
        
def load(grid) -> int:
    nrow, ncol = len(grid), len(grid[0])
    return sum(
        nrow - r if grid[r][c] == "O" else 0
        for r, c in product(nrow, ncol)
    )
    
def solve1(sections: list[list[str]]) -> int:
    grid = list(map(list, sections[0]))
    nrow, ncol = len(grid), len(grid[0])
    #pprint(grid)
    for col in range(0, ncol): slide_north(grid, col)
    print()
    #pprint(grid)
    
    return load(grid)

def solve2(sections: list[list[str]], expand=5) -> int:
    return -1

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***', solve1(sections))
    
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
