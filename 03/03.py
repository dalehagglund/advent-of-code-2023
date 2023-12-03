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
    def adjacent_to_sym(row, start, end):
        for col in range(start, end):
            for drow, dcol in product((-1, 0, 1), (-1, 0, 1)):
                r, c = row + drow, col + dcol
                if r < 0 or r >= nrow: continue
                if c < 0 or c >= ncol: continue
                if lines[r][c] not in non_symbols:
                    return True
        return False
        
    total = 0
    for row, line in enumerate(lines):
        for m in re.finditer(r"\d+", line):
            if adjacent_to_sym(row, m.start(0), m.end(0)):
                total += int(m.group(0))

    print('part sum', total)
    
def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***')

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
