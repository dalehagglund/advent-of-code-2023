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
    reduce
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
            
    def _find_position(self, n):
        for i, (lo, hi) in enumerate(self.indices):
            if n < hi: return i
        else:
            return len(self.indices)
            
    def translate_ranges(self, rset: set[Range]) -> set[Range]:
        result = set()
        for r in rset:
            result.update(self.translate_range(r))
        return result

    def translate_range(self, r: Range) -> set[Range]:
        print(f'> Map.translate_range({self.source}, {self.dest}): {r = }')
        def intersect(r1: Range, r2: Range) -> ty.Optional[Range]:
            r1, r2 = (r1, r2) if r1[0] <= r2[0] else (r2, r1)
            r1lo, r1hi = r1
            r2lo, r2hi = r2
            assert r1lo <= r2lo

            if r2lo >= r1hi: return None
            interval = ( max(r1lo, r2lo), min(r1hi, r2hi) )
            if interval[0] == interval[1]: return None
            return interval
            
        def adjust_intersection(index, r: Range) -> Range:
            delta = self.ranges[index][0] - index[0]
            return (r[0] + delta, r[1] + delta)
            
        s = iter(self.indices)
        s = map(lambda index: (index, intersect(r, index)), s)
        s = filter(star(lambda _, intersection: intersection is not None), s)
        s = map(star(adjust_intersection), s)
        #s = sorted(s)
        #return merge_intervals(s)            
        return set(s)  
    
def parse_sections(sections: list[list[str]]):
    initial_seeds = list(map(int, re.split(r"[- ]", sections[0][0])[1:]))

    maps = dict()
    for sec in sections[1:]:
        m = Map(sec)
        maps[m.source] = m
        
    assert len(maps) == len(sections[1:])
    return initial_seeds, maps
 
def solve1(sections: list[list[str]]) -> int:
    from pprint import pprint
    
    initial_seeds, maps = parse_sections(sections)

    def translate(source, dest, value):
        m = maps[source]
        while m.dest != dest:
            value = m.translate(value)
            m = maps[m.dest]
        return m.translate(value)

    s = map(partial(translate, 'seed', 'location'), initial_seeds)
    return min(itertools.chain([float('-inf')], s))
    
def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***', solve1(sections))
    
def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch

def solve2(sections: list[list[str]]) -> int:
    from pprint import pprint
    
    initial_seeds, maps = parse_sections(sections)

    s = iter(initial_seeds)
    s = batched(s, 2)
    s = map(tuple, s)
    s = observe(print, s)
    s = map(star(lambda lo, n: (lo, lo + n)), s) # half-open intervals
    seed_ranges = set(s)
    
    pprint(seed_ranges)
    
    def expand(source, dest, ranges):
        print('> expand', source, dest)
        
        m = maps[source]
        while m.dest != dest:
            print(f'   > {m.dest = } {ranges = }')
            ranges = m.translate_ranges(ranges)
            m = maps[m.dest]
        ranges = m.translate_ranges(ranges)
        return m.translate_ranges(ranges)

    location_ranges = expand('seed', 'location', seed_ranges)

    pprint(location_ranges)`

    return min(r[0] for r in location_ranges)

def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve2(sections))

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
