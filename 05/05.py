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

Range = tuple[int, int]

@dataclass
class Map:
    source: str
    dest: str
    ranges: dict[Range, Range]
    indices: list[Range]
    
    def __init__(self, lines):
        title, *rest = lines
        self.source, _, self.dest, *_ = re.split(r"[- ]", title)
        s = iter(rest)
        s = map(str.split, s)
        s = map(partial(map, int), s)
        s = map(tuple, s)
        self.ranges = dict(
            ((src_start, src_start + n), (dst_start, dst_start + n))
            for dst_start, src_start, n
            in s
        )
        self.indices = sorted(self.ranges.keys())

    def translate(self, i):
        #print(f'> translate: {i = }')
        for slo, shi in self.indices:
            if not (slo <= i < shi): continue
            delta = i - slo
            #print(f'> translate: found {(slo, shi) = } {delta = }')
            dlo, dhi = self.ranges[(slo, shi)]
            return dlo + delta
        else:
            return i
        pass
 
def solve1(sections: list[list[str]]) -> int:
    from pprint import pprint
    
    initial_seeds = list(map(int, re.split(r"[- ]", sections[0][0])[1:]))
    print("> ", initial_seeds)
    maps = dict()
    for sec in sections[1:]:
        m = Map(sec)
        maps[m.source] = m
        
    assert len(maps) == len(sections[1:])

    def translate(source, dest, value):
        m = maps[source]
        while m.dest != dest:
            value = m.translate(value)
            m = maps[m.dest]
        return m.translate(value)
        
    print(f"> {translate('seed', 'location', 14) = }")

    s = map(partial(translate, 'seed', 'location'), initial_seeds)
    return min(s)
    
def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***', solve1(sections))

def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***')

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
