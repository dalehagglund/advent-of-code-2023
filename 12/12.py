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


def solve1(sections: list[list[str]]) -> int:
    rows = []
    for i, line in enumerate(sections[0]):
        pattern, right = line.split()
        groups = list(map(int, right.split(",")))
        qpositions = [
            m.start()
            for m in
            re.finditer(r'\?', pattern)
        ]
        assert len(qpositions) > 0, f'line {i}: no ? marks'
        rows.append((qpositions, pattern, groups))
        
    def replace(orig: list[str], replacements) -> list[str]:
        new = orig.copy()
        for pos, newchar in replacements:
            new[pos] = newchar
        return new
    
    broken = re.compile(r'#+')
    def matches_groups(groups, s: str) -> bool:
        lengths = list(map(len, broken.findall(s)))
        #print('> matches_groups:', s, groups, lengths)
        return lengths == groups        
    
    total = 0
    for i, (positions, pat, groups) in enumerate(rows):
        exploded = list(pat)
                
        s = itertools.product("#.", repeat=len(positions))
        s = map(partial(zip, positions), s)
        s = map(tuple, s)
        #s = observe(partial(print, '#1'), s)
        s = map(partial(replace, exploded), s)
        s = map(partial(''.join), s)
        #s = observe(partial(print, '#2'), s)
        s = map(partial(matches_groups, groups), s)
        count = sum(s)
        total += count
        
        print(f'{i}: {count = } {pat = } {groups = }')
    
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
