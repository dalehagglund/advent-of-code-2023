import sys
import typing as ty
from dataclasses import dataclass, field
from enum import Enum
import collections
import re
import itertools
from itertools import (
    islice,
    product,
    pairwise,
    zip_longest
)
from functools import (
    partial
)

from tools import *

@dataclass
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0
    
@dataclass
class Game:
    id: int
    draws: list[Draw] = field(default_factory=list)

def parse_draw(s: str) -> Draw:
    counts = dict(red=0, green=0, blue=0)
    for sample in s.split(", "):
        count, color = sample.split(" ")
        counts[color] = int(count)
    return Draw(**counts)

def parse_game(s: str) -> Game:
    game_spec, draw_specs = s.split(": ")

    game_id = int(game_spec.split(' ')[1])
    game = Game(id=game_id)

    for draw_spec in draw_specs.split("; "):
        game.draws.append(parse_draw(draw_spec))

    return game
    
def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***')

    maxbag = Draw(red=12, green=13, blue=14)
    
    def possible_draw(d: Draw) -> bool:
        return (
            d.red <= maxbag.red and
            d.green <= maxbag.green and
            d.blue <= maxbag.blue
        )
    def possible_game(g: Game) -> bool:
        return all(possible_draw(d) for d in g.draws)
    
    s = iter(sections[0])
    s = map(parse_game, s)
    s = filter(possible_game, s)
    
    print('sum', sum(g.id for g in s))
    
def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***')

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
    