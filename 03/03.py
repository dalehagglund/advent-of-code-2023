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
    partial
)

from tools import *

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***')
    lines = sections[0]
    nrow = len(lines)
    ncol = len(lines[0])

    non_symbols = set("0123456789.")    

    def is_symbol(c: str): return c not in non_symbols

    all_symbols = set(
        (r, c)
        for r, c
        in product(nrow, ncol)
        if is_symbol(lines[r][c])
    )
    
    def number_locations():
        for row, line in enumerate(lines):
            for m in re.finditer(r"\d+", line):
                yield (int(m.group()), row, m.start(), m.end())

    def adjacent_cells(row, start, end):
        s = itertools.chain(
            ((row - 1, col) for col in range(start, end)),
            ((row + 1, col) for col in range(start, end)),
            ((r, start - 1) for r   in (row - 1, row, row + 1)),
            ((r, end      ) for r   in (row - 1, row, row + 1))
        )
        s = filter(star(lambda r, _: r >= 0 and r < nrow), s)
        s = filter(star(lambda _, c: c >= 0 and c < ncol), s)
        return set(s)
        
    parts = []
    gears = collections.defaultdict(list)

    for n, row, start, end in number_locations():
        adjacent = adjacent_cells(row, start, end)
        syms = adjacent & all_symbols
        if len(syms) > 0:
            parts.append(n)
        for r, c in syms:
            if lines[r][c] != "*": continue
            gears[(r, c)].append(n)
            
    print('part sum', sum(parts))
    print('ratio sum',
        sum(
            mul(parts)
            for gear, parts
            in gears.items()
            if len(parts) == 2
        )
    )

def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***')

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
