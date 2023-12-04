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
    #s = observe(print, s)
    return sum(s)

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***')
    print('part 1 answer', solve1(sections[0]))

def solve2(lines: list[str]) -> int:
    cards = list(map(parse_card, lines))
    cards.insert(0, None) # align index with card number

    copies = [1] * len(cards)
    copies[0] = 0
    
    matches = list(
        (len(c.draws & c.winning) if c else 0)
        for c
        in cards
    )
    
    print('>> cards', '\n'.join(map(str, cards)))

    print('>> matches', matches)
    print('>> copies', copies)
    
    for id in range(1, len(cards)):
        count = copies[id]
        inc = matches[id]
        print(f'>> card {id} count {count} matches {inc}')

        for n in range(1, inc+1):
            copies[id + n] += count
            
        print(f'>> after {id} copies', copies)
    
    return sum(copies)

def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***')
    print('part 2 answer', solve2(sections[0]))

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
