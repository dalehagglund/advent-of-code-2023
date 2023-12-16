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

def show_grid(grid: np.array, indent: int = 4):
    nrows, ncols = grid.shape
    prefix = " " * indent
    for line in map(''.join, (list(grid[r, :]) for r in range(nrows))):
        print(f'{prefix}{line}')

Point = tuple[int, int]

class Point(ty.NamedTuple):
    r: int
    c: int
    
    def __add__(self, other):
        iter(self)
        iter(other)
        r, c = map(operator.add, self, other)
        return Point(r, c)

class Dir:
    U = (-1,  0)
    D = (+1,  0)
    L = ( 0, -1)
    R = ( 0, +1)
    
pass_through_dirs = {
    '-': (Dir.L, Dir.R),
    '|': (Dir.U, Dir.D),
}

split = {
    ('-', Dir.U): (Dir.L, Dir.R),
    ('-', Dir.D): (Dir.L, Dir.R),
    ('-', Dir.L): (Dir.L,),
    ('-', Dir.R): (Dir.R,),

    ('|', Dir.U): (Dir.U,),
    ('|', Dir.D): (Dir.D,),
    ('|', Dir.L): (Dir.U, Dir.D),
    ('|', Dir.R): (Dir.U, Dir.D),
}

reflect = {
    ('/',  Dir.U): Dir.R,
    ('/',  Dir.D): Dir.L,
    ('/',  Dir.L): Dir.D,
    ('/',  Dir.R): Dir.U,

    ('\\', Dir.U): Dir.L,
    ('\\', Dir.D): Dir.R,
    ('\\', Dir.L): Dir.U,
    ('\\', Dir.R): Dir.D,
}

def follow_beam(grid, startpos, startdir):
    nrows, ncols = grid.shape
    
    queue = collections.deque()
    seen = set()
    queue.appendleft((startpos, startdir))
    while len(queue) > 0:
        curpos, curdir = queue.popleft()
        if (curpos, curdir) in seen:
            continue
        seen.add((curpos, curdir))
        r, c = curpos
        in_bounds = (0 <= r < nrows and 0 <= c < ncols)
        if not in_bounds:
            continue

        yield curpos, curdir    

        at_pos = grid[curpos]
        if at_pos == '.':
            queue.appendleft((curpos + curdir, curdir))
        elif at_pos in '''-|''':
            for nextdir in split[(at_pos, curdir)]:
                queue.appendleft((curpos + nextdir, nextdir))
        elif at_pos in '''\/''':
            nextdir = reflect[(at_pos, curdir)] 
            queue.appendleft((curpos + nextdir, nextdir))
        else:
            assert False, f"unexpected char at {curpos = }: {at_pos = }"
    
def make_grid(lines: list[str]) -> np.array:
    return np.array(list(map(list, lines)))

def solve1(sections: list[list[str]]) -> int:
    grid = make_grid(sections[0])
    show_grid(grid)
    counts = np.zeros(grid.shape)

    for point, dir in follow_beam(grid, Point(0, 0), Dir.R):
        #print(point, dir)
        counts[point] += 1
        
    print(counts)
    
    return np.sum(counts > 0)

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
