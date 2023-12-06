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
            
    def shift(self, shift):
        return Interval(self.lo + shift, self.hi + shift)

@dataclass
class Map:
    _source: str
    _dest: str
    _shift: dict[Interval, int]
    _indices: list[Interval]
        
    def source(self): return self._source
    def dest(self): return self._dest
    
    def map(self, n: int) -> int:
        for iv in self._indices:
            if iv.lo <= n < iv.hi:
                return n + self._shift[iv]
        assert "didn't expect to exit the loop"
    
    def map_interval(self, interval: Interval) -> \
            ty.Iterator[Interval]:
        lo, hi = interval.lo, interval.hi
        
        indices = iter(self._indices)
        src_iv = next(indices)

        #print(f'> map_intv: {(lo, hi) = }')
        while lo < hi:
            #print(f'   > {(lo, hi) = } {src_iv = }')
            if lo >= src_iv.hi: 
                #print('   > skip')
                src_iv = next(indices)
                continue
            assert lo >= src_iv.lo

            prefix = Interval( max(lo, src_iv.lo), min(hi, src_iv.hi) )
            assert prefix.hi - prefix.lo > 0
            assert prefix.lo == lo
            assert prefix.hi <= hi
            assert src_iv.lo <= prefix.lo < src_iv.hi
            assert src_iv.lo <= prefix.hi <= src_iv.hi
            
            delta = self._shift[src_iv]
            dst_iv = prefix.shift(delta)
            
            #print(f'   > {delta = } {prefix = } {dst_iv = }')
            yield dst_iv

            lo = prefix.hi

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
        #s = observe(partial(print, "#1"), s)
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
        
        #print("#10: source", pp.pformat(source))
        #print("#10: dest  ", pp.pformat(dest))
        #print("#10: shift ", pp.pformat(shift))
        #print("#10: indices", pp.pformat(indices))
                
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
    initial_seeds, maps = parse_sections(sections)


    s = iter(initial_seeds)
    s = chunked(s, 2)
    s = map(tuple, s)
    #s = observe(print, s)
    s = map(star(lambda lo, n: Interval(lo, lo + n)), s) # half-open intervals
    seed_ranges = set(s)

    print('> initial_seeds ', pp.pformat(initial_seeds))
    print('> seed ranges ', pp.pformat(seed_ranges))
    #print('> maps ', pp.pformat(maps))
 
    def expand(m: Map, intervals: list[Interval]) -> list[Interval]:
        print(f'> expand: m = {pp.pformat(m)}') 
        print(f'> expand: {intervals = }')
        s = iter(intervals)
        s = map(m.map_interval, s)
        s = itertools.chain.from_iterable(s)
        newintervals = list(s)
        
        print(f'> expand: {newintervals = }')
        return newintervals
        
    def follow(src, dst, intervals: list[Interval]) -> list[Interval]:
        print(f'> follow: {src = } {dst = } {intervals = }')
        m = maps[src]
        while m.dest() != dst:
            intervals = expand(m, intervals)
            m = maps[m.dest()]
        intervals = expand(m, intervals)
        return intervals

    test_intervals = [
        Interval(79, 79 + 14),
        Interval(55, 55 + 13),
    ]
    
    
    output_intervals = follow('seed', 'location', seed_ranges)
    print(min(output_intervals, key=lambda iv: iv.lo))

    return -1

def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve2(sections))

if __name__ == '__main__':
    #part1(sys.argv[1])
    part2(sys.argv[1])
