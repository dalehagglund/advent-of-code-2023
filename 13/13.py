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

swap_char = dict(zip("#.", ".#"))
    
def find_refl_lines(grid, nrow, ncol, smudge=None) -> ty.Optional[int]:
    # think of refpos as a cursor between two colummns,
    # ie if refpos is, eg, 3, the reflection line runs
    # vertically between column indices 2 and 3

    def apply_smudge(r, c):
        if smudge is None: return grid[r][c]
        if smudge != (r, c): return grid[r][c]
        return swap_char[grid[r][c]]

    def column(i):
        return ''.join(
            apply_smudge(r, i) 
            for r in range(nrow)
        )
    def row(i):
        return ''.join(
            apply_smudge(i, c)
            for c in range(ncol)
        )

    def reflects_about(get, pos, width) -> bool:
        s = range(width)
        s = map(lambda i: get(pos - i - 1) == get(pos + i), s)
        return all(s)

    def candidates(get, maxpos, positions):        
        s = iter(positions)
        s = filter(lambda p: get(p-1) == get(p), s)
        s = map(lambda p: (p, min(maxpos - p, p)), s)
        #s = observe(partial(print, 'candidates: possible'), s)
        s = filter(star(partial(reflects_about, get)), s)
        s = map(partial(nth, 0), s)
        return set(s)
 
    vset = candidates(column, ncol, range(1, ncol))
    hset = candidates(row, nrow, range(1, nrow))    

    #print(f'refl({smudge=}): final: {vset = } {hset = }')
    if not smudge:
        assert len(vset) <= 1
        assert len(hset) <= 1
        assert len(hset) != len(vset)
    
    for pos in vset: yield ('vert', pos)
    for pos in hset: yield ('horz', pos)

def score(kind, pos):
    if kind == 'vert': return pos
    if kind == 'horz': return 100 * pos
    assert False, "shouldn't get here"

def solve1(sections: list[list[str]]) -> int:
    s = iter(sections)
    s = map(lambda g: (g, len(g), len(g[0])), s)
    s = map(star(find_refl_lines), s)
    s = map(set, s)
    s = map(set.pop, s)
    s = map(star(score), s)
    return sum(s)
    
def mapf(*funcs):
    def _exec(*args):
        return tuple(f(*args) for f in funcs)
    return _exec

def solve2(sections: list[list[str]], expand=5) -> int:
    def apply_smudges(grid, nrow, ncol):
        orig = set(find_refl_lines(grid, nrow, ncol))
        smudged = set()
        for r, c in product(nrow, ncol):
            smudged |= set(find_refl_lines(grid, nrow, ncol, smudge=(r, c)))
        new = smudged - orig
        print(f'solve2: {orig = } {smudged = } {new = }')
        assert len(new) == 1
        return new.pop()
    s = iter(sections)
    s = observe(pprint, s)
    s = map(lambda g: (g, len(g), len(g[0])), s)
    s = map(star(apply_smudges), s)
    s = map(star(score), s)
    return sum(s)
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
