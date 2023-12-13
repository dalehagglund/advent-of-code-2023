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
import contextlib
import time
import operator

from tools import *

def parse_rows(lines: list[str], part2=False):
    rows = []

    for i, line in enumerate(lines):
        pattern, right = line.split()
        groups = list(map(int, right.split(",")))
        qpositions = [
            m.start()
            for m in
            re.finditer(r'\?', pattern)
        ]
        if not part2:
            assert len(qpositions) > 0, f'line {i}: no ? marks'
        rows.append((qpositions, pattern, groups))

    return rows

def solve1(sections: list[list[str]]) -> int:
    rows = parse_rows(sections[0])
    
    total = 0
    for i, (positions, s, groups) in enumerate(rows):
        print(f'{i}: {s = } {groups = }')
        # count = 0
        # for assignment in backtrack(s, {}, 0, groups, 0):
            # #print(f'   > {assignment = }') 
            # count += 1
        count = count_possible(s, {}, 0, groups, 0)
        print(f'>   {count = }')
        total += count
    
    return total

@contextlib.contextmanager
def update(assignment, key, val):
    assert key not in assignment
    assignment[key] = val
    try:
        yield
    finally:
        del assignment[key]

def count_possible(s, assignment, runlen, lengths, pos) -> int:
    assert 0 <= pos <= len(s)    

    ### base case: we've hit the end of the pattern string
    
    if pos == len(s) and len(lengths) == 0:
        return 1
    if pos == len(s) and len(lengths) == 1:
        if runlen == lengths[0]: return 1
        return 0
    if pos == len(s) and len(lengths) > 1:
        return 0

    assert 0 <= pos < len(s)
    assert s[pos] in ('.', '?', '#')
    
    ### we've run out of lengths

    if len(lengths) == 0 and s[pos] == '.':
        return count_possible(s, assignment, 0, lengths, pos + 1)
    if len(lengths) == 0 and s[pos] == '?':
        with update(assignment, pos, '.'):
            return count_possible(s, assignment, 0, lengths, pos + 1)
        return
    if len(lengths) == 0 and s[pos] == '#':
        return 0

    assert len(lengths) > 0
    nextlen = lengths[0]
    assert nextlen > 0
    assert runlen <= nextlen
    
    ### still looking for a run

    if runlen == 0 and s[pos] == '.':
        # no run to start, so advance
        return count_possible(s, assignment, 0, lengths, pos + 1)
    if runlen == 0 and s[pos] == '#':
        # must force a run to begin
        return count_possible(s, assignment, 1, lengths, pos + 1)
    if runlen == 0 and s[pos] == '?':
        # no run so far, try both alternatives
        with update(assignment, pos, '.'):
            possible_as_dot = count_possible(s, assignment, 0, lengths, pos + 1)        
        with update(assignment, pos, '#'):
            possible_as_broken = count_possible(s, assignment, 1, lengths, pos + 1)
        return possible_as_dot + possible_as_broken
        
    ### run is short of curent expected length
    
    if runlen < nextlen and s[pos] == '.':
        # run ends too soon, abandon search
        return 0
    if runlen < nextlen and s[pos] == '#':
        # required to extend run, continue search
        return count_possible(s, assignment, runlen + 1, lengths, pos + 1)
    if runlen < nextlen and s[pos] == '?':
        # must force ? to '#' to continue the run
        with update(assignment, pos, '#'):
            return count_possible(s, assignment, runlen + 1, lengths, pos + 1)

    ### run has hit the current expected length
    
    if runlen == nextlen and s[pos] == '.':
        # consume expected length, keep looking
        return count_possible(s, assignment, 0, lengths[1:], pos + 1)
    if runlen == nextlen and s[pos] == '#':
        # run is now long, abandon this search
        return 0
    if runlen == nextlen and s[pos] == '?':
        # have to end the run, so assign '.' to pos
        with update(assignment, pos, '.'):
            return count_possible(s, assignment, 0, lengths[1:], pos + 1)
    
    assert False, "Not expected to get here!"

def backtrack(s, assignment, runlen, lengths, pos):
    assert 0 <= pos <= len(s)    

    ### base case: we've hit the end of the pattern string
    
    if pos == len(s) and len(lengths) == 0:
        yield assignment.copy()
        return
    if pos == len(s) and len(lengths) == 1:
        if runlen == lengths[0]: yield assignment.copy()
        return
    if pos == len(s) and len(lengths) > 1:
        return

    assert 0 <= pos < len(s)
    assert s[pos] in ('.', '?', '#')
    
    ### we've run out of lengths

    if len(lengths) == 0 and s[pos] == '.':
        yield from backtrack(s, assignment, 0, lengths, pos + 1)
        return
    if len(lengths) == 0 and s[pos] == '?':
        with update(assignment, pos, '.'):
            yield from backtrack(s, assignment, 0, lengths, pos + 1)
        return
    if len(lengths) == 0 and s[pos] == '#':
        return

    assert len(lengths) > 0
    nextlen = lengths[0]
    assert nextlen > 0
    assert runlen <= nextlen
    
    ### still looking for a run

    if runlen == 0 and s[pos] == '.':
        # no run to start, so advance
        yield from backtrack(s, assignment, 0, lengths, pos + 1)
        return
    if runlen == 0 and s[pos] == '#':
        # must force a run to begin
        yield from backtrack(s, assignment, 1, lengths, pos + 1)
        return
    if runlen == 0 and s[pos] == '?':
        # no run so far, try both alternatives
        with update(assignment, pos, '.'):
            yield from backtrack(s, assignment, 0, lengths, pos + 1)        
        with update(assignment, pos, '#'):
            yield from backtrack(s, assignment, 1, lengths, pos + 1)
        return
        
    ### run is short of curent expected length
    
    if runlen < nextlen and s[pos] == '.':
        # run ends too soon, abandon search
        return
    if runlen < nextlen and s[pos] == '#':
        # required to extend run, continue search
        yield from backtrack(s, assignment, runlen + 1, lengths, pos + 1)
        return
    if runlen < nextlen and s[pos] == '?':
        # must force ? to '#' to continue the run
        with update(assignment, pos, '#'):
            yield from backtrack(s, assignment, runlen + 1, lengths, pos + 1)
        return

    ### run has hit the current expected length
    
    if runlen == nextlen and s[pos] == '.':
        # consume expected length, keep looking
        yield from backtrack(s, assignment, 0, lengths[1:], pos + 1)
        return
    if runlen == nextlen and s[pos] == '#':
        # run is now long, abandon this search
        return
    if runlen == nextlen and s[pos] == '?':
        # have to end the run, so assign '.' to pos
        with update(assignment, pos, '.'):
            yield from backtrack(s, assignment, 0, lengths[1:], pos + 1) 
        return
    
    assert False, "Not expected to get here!"

def solve2(sections: list[list[str]], expand=5) -> int:
    rows = parse_rows(sections[0], part2=True)
    
    total = 0
    start_time = lap_start = time.time()
    for i, (positions, s, groups) in enumerate(rows):
        start = time.time()
        new_s = '?'.join(s for _ in range(expand))
        new_groups = groups * expand
        print(f'{i}: {s = } {groups = } {expand = }')
        # count = 0
        # for assignment in backtrack(new_s, {}, 0, new_groups, 0):
            # #print(f'   > {assignment = }')
            # count += 1
        count = count_possible(new_s, {}, 0, new_groups, 0)
        
        elapsed_time = int(time.time() - start_time)
        t = time.time()
        lap_time = int(t - lap_start)
        lap_start = t
        print(f'>   {count = }')
        print(f'>   {lap_time = } {elapsed_time = }')
        total += count
    
    return total

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
