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

    def adjacent_syms(row, start, end):
        syms = set()
        for col in range(start, end):
            for drow, dcol in product((-1, 0, 1), (-1, 0, 1)):
                r, c = row + drow, col + dcol
                if r < 0 or r >= nrow: continue
                if c < 0 or c >= ncol: continue
                if lines[r][c] not in non_symbols:
                    syms.add((r, c, lines[r][c]))
        return syms
        
    parts = []
    gears = collections.defaultdict(lambda: [])
    for row, line in enumerate(lines):
        for m in re.finditer(r"\d+", line):
            adjacent = adjacent_syms(row, m.start(0), m.end(0))
            if len(adjacent) == 0:
                continue
            partnum = int(m.group(0))
            if len(adjacent) > 0:
                parts.append(partnum)
            for r, c, symbol in adjacent:
                if symbol != "*": continue
                gears[(r, c)].append(partnum)

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
