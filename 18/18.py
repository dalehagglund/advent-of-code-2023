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

Point = tuple[int, int]

class Point(ty.NamedTuple):
    r: int
    c: int
    
    def __add__(self, other):
        iter(self)
        iter(other)
        r, c = map(operator.add, self, other)
        return Point(r, c)
    def __sub__(self, other):
        iter(self)
        iter(other)
        r, c = map(operator.sub, self, other)
        return Point(r, c)
    
class Dir:
    U = (-1,  0)
    D = (+1,  0)
    L = ( 0, -1)
    R = ( 0, +1)

def show_grid(grid: list[str], indent=4):
    for line in grid:
        print(f'{" " * indent}{line}')
    
def make_grid(lines: list[str]) -> np.array:
    ncol = len(lines[0])
    return np.array(
        list(
            itertools.chain(
                ['.' * (ncol + 2)],
                list(map(lambda t: '.' + t + '.', lines)),
                ['.' * (ncol + 2) ]
            )
        )
    )
    
def parse_instructions(lines: list[str], part2=False):
    dirmap_1 = dict(zip('UDLR', [Dir.U, Dir.D, Dir.L, Dir.R]))
    dirmap_2 = dict(zip('0123', [Dir.R, Dir.D, Dir.L, Dir.U]))
    
    def convert_2(dir, n, hexcode):
        dist = int(hexcode[:5], base=16)
        dir = dirmap_2[hexcode[-1]]
        return (dir, dist, None)
    def convert_1(dir, n, hexcode):
        return (dirmap_1[dir], int(n), None)

    s = iter(lines)
    s = map(partial(re.split, r"[ #()]+"), s)
    #s = observe(print, s)
    s = map(lambda t: t[:3], s)
    s = map(star(convert_2 if part2 else convert_1), s)
    #s = observe(print, s)
    return s
    
def create_grid(instructions):
    start = here = Point(0, 0)
    cells = { here }
    
    for dir, steps, _ in instructions:
        for i in range(steps):
            here = here + dir
            assert here == start or here not in cells, f'{(dir, steps, i, here) = }'
            cells.add(here)
            
    #pprint(cells)
    
    minrow = min(cells, key=lambda p: p.r).r
    maxrow = max(cells, key=lambda p: p.r).r
    mincol = min(cells, key=lambda p: p.c).c
    maxcol = max(cells, key=lambda p: p.c).c
    print(f'{(minrow, maxrow, mincol, maxcol) = }')

    assert maxrow >= minrow and maxcol >= mincol
    nrow = maxrow - minrow + 1
    ncol = maxcol - mincol + 1
    print(f'{(nrow, ncol) = }')
    
    grid = np.full((nrow + 2, ncol + 2), '.')
    s = iter(cells)
    s = map(lambda p: p - (minrow, mincol), s)
    s = map(lambda p: p + (1, 1), s)
    for pos in s:
        grid[pos] = '#'
    return grid

def show_grid(grid, indent=4):
    for row in grid:
        print(f"{' ' * indent}{''.join(row)}")

def flood_fill(grid, start):
    nrow, ncol = grid.shape
    queue = collections.deque()
    queue.append(start)
    visited = set()
    while len(queue) > 0:
        #print(f'#1: {len(queue) = }')
        node = queue.popleft()
        if node in visited: continue

        #grid[node] = '*'
        #show_grid(grid)
        grid[node] = 'E'
        
        visited.add(node)
        s = [Dir.U, Dir.D, Dir.L, Dir.R]
        s = map(lambda d: node + d, s)
        s = filter(lambda p: 0 <= p.r < nrow, s)
        s = filter(lambda p: 0 <= p.c < ncol, s)
        for n in s:
            #assert (grid[n] in '#E') == (n in visited) 
            #if grid[n] in 'E#': continue
            if grid[n] == "#": continue
            queue.append(n)

def solve1(sections: list[list[str]]) -> int:
    instructions = list(parse_instructions(sections[0]))
    return -1
    grid = create_grid(instructions)
    perimeter = np.sum(grid == '#')
    flood_fill(grid, Point(0, 0))
    return perimeter + np.sum(grid == '.')

# This is supposed to be numpy magic to compute the polygon area
# from a lists of x and y co-ords respectively, but it didn't seem 
# to work for me.
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def solve2(sections: list[list[str]]) -> int:
    instructions = list(parse_instructions(sections[0], part2=True))

    B = 0
    points = [Point(0, 0)]
    for dir, steps, _ in instructions:
        start = points[-1]
        v = (dir[0] * steps, dir[1] * steps)
        B += steps
        #print(f'{(start, dir, steps, v) = }')
        points.append(start + v)
    assert B % 2 == 0

    # The trapezoid form of the "Shoelace Formula".
    # https://en.wikipedia.org/wiki/Shoelace_formula#Trapezoid_formula

    A = 0
    for p1, p2 in itertools.pairwise(points):
        A += (p1.r + p2.r) * (p1.c - p2.c)
    assert A % 2 == 0  # seems to be true, but I don't know why
    A //= 2
        
    # Pick's theorem says that for an polygon with
    # integer vertices the total area A is
    #
    #     A = I + B/2 - 1
    #
    # where
    #
    #     I: the number of lattice points in the interior, which in our
    #        case of integral vertices, has to be the same as the Area
    #     B: the number of lattice points on the bounding 
    #
    # So, 
    #
    #     I = A - B/2 + 1
    #
    # and the total number of lattice points (ie, how many cubes have been
    # dug out) is
    #
    #     I + B
    
    I = A - B//2 + 1
    return I + B
    
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
