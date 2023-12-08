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

from tools import *
from camel import Hand

def read_bids(
        sec: list[str],
        wild=False,
    ) -> list[tuple[str, int]]:
    
    make_hand = partial(Hand, wild=wild)
    s = iter(sec)
    s = map(str.split, s)
    s = map(partial(convert_fields, (make_hand, int)), s)
    return list(s)
    
def solve1(sections, wild=False) -> int:
    ordered_hands = sorted(
        read_bids(sections[0], wild=wild),
        key=partial(nth, 0)
    )
    return sum(
        rank * bid
        for rank, (card, bid) 
        in zip(itertools.count(1), ordered_hands)
    )

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***', solve1(sections, wild=False))
    
def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve1(sections, wild=True))

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
