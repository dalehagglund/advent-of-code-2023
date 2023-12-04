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

@dataclass
class Card:
    id: int = 0
    winning: set[int] = field(default_factory=set)
    draws: set[int] = field(default_factory=set)

def parse_card(line: str) -> Card:
    #print(">", line)
    card, left, right = re.split(r"\s*[:|]\s*", line)
    id = int(card.split()[1])
    winning = list(map(int, left.split()))
    draws = list(map(int, right.split()))

    assert len(set(winning)) == len(winning)
    assert len(set(draws)) == len(draws)

    return Card(
        id=id,
        winning=set(winning),
        draws=set(draws)
    )

def solve1(lines: list[str]) -> int:    
    s = iter(lines)
    s = map(parse_card, s)
    s = map(lambda c: len(c.draws & c.winning), s)
    s = map(lambda n: 2**(n-1) if n > 0 else 0, s)
    s = observe(print, s)
    return sum(s)

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***')
    print('part 1', solve1(sections[0]))


def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***')

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
