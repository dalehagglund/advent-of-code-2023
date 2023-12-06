import sys
import typing as ty
import dataclasses
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
import pprint

from tools import *

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)

@dataclass(frozen=True)
class Interval:
    lo: int
    hi: int
    
    def __post_init__(self):
        if not(self.lo <= self.hi):
            raise ValueError("Interval: 'lo' larger than 'hi'")

@dataclass
class Map:
    _source: str
    _dest: str
    _shift: dict[Interval, int]
    _indices: list[Interval]
        
    def source(self): return self._source
    def dest(self): return self._dest

    @classmethod
    def from_section(cls, lines) -> ty.Self:
        title, *rest = lines
        source, _, dest, *_ = re.split(r"[- ]", title)

        minint, maxint = 0, 2**33
        
        def in_range(n: int) -> bool:
            return minint <= n <= maxint
        def assert_in_range(n: int):
           if not in_range(n):
               raise ValueError(f'{n = } not in interval [{minint}, {maxint})')
        def assert_valid_triple(dst_start: int, src_start: int, n: int):
            assert n > 0, "expecting the mapped interval to be non-empty"
            for i in (dst_start, src_start, n):
                assert_in_range(i)
            assert_in_range(dst_start + n)
            assert_in_range(src_start + n)

        s = iter(rest)
        s = map(str.split, s)
        s = map(partial(map, int), s)
        s = map(tuple, s)
        s = observe(partial(print, "#1"), s)
        s = observe(star(assert_valid_triple), s)         
        s = sorted(s, key=partial(nth, 1))
        
        shift = {}
        indices = []

        def add_index(interval: Interval, delta):
            indices.append(interval)
            shift[interval] = delta

        for curtuple in s:
            curdst, cursrc, n = curtuple
            delta = curdst - cursrc
            cur = Interval(cursrc, cursrc + n)
            
            if len(indices) == 0 and cur.lo == minint:
                add_index(cur, delta)
                continue
                
            if len(indices) == 0 and cur.lo > minint:
                add_index(Interval(minint, cur.lo), 0)
                
            if indices[-1].hi < cur.lo:
                gap = Interval(indices[-1].hi, cur.lo)
                add_index(gap, 0)
            add_index(cur, delta)
            
        add_index(Interval(indices[-1].hi, maxint), 0)
        
        print("#10: source", pp.pformat(source))
        print("#10: dest  ", pp.pformat(dest))
        print("#10: shift ", pp.pformat(shift))
        print("#10: indices", pp.pformat(indices))
                
        return cls(source, dest, shift, indices)        
    
def parse_sections(sections: list[list[str]]):
    initial_seeds = list(map(int, re.split(r"[- ]", sections[0][0])[1:]))

    maps = dict()
    for sec in sections[1:]:
        m = Map.from_section(sec)
        maps[m.source()] = m
        
    assert len(maps) == len(sections[1:])
    return initial_seeds, maps
    
def solve2(sections: list[list[str]]) -> int:
    from pprint import pprint
    
    initial_seeds, maps = parse_sections(sections)


    s = iter(initial_seeds)
    s = chunked(s, 2)
    s = map(tuple, s)
    s = observe(print, s)
    s = map(star(lambda lo, n: (lo, lo + n)), s) # half-open intervals
    seed_ranges = set(s)

    print('> initial_seeds ', pp.pformat(initial_seeds))
    print('> seed ranges ', pp.pformat(seed_ranges))
    print('> maps ', pp.pformat(maps))
    
    return -1

def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve2(sections))

if __name__ == '__main__':
    #part1(sys.argv[1])
    part2(sys.argv[1])
