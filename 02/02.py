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

    testbag = Draw(red=12, green=13, blue=14)
    
    def possible_draw(d: Draw) -> bool:
        return (
            d.red <= testbag.red and
            d.green <= testbag.green and
            d.blue <= testbag.blue
        )
    def possible_game(g: Game) -> bool:
        return all(possible_draw(d) for d in g.draws)
    
    s = iter(sections[0])
    s = map(parse_game, s)
    games = collect(list, s)
    
    print('sum of possible', sum(g.id for g in games if possible_game(g)))
    
    def minbag(g: Game) -> Draw:
        return Draw(
            red = max(d.red for d in g.draws),
            green = max(d.green for d in g.draws),
            blue = max(d.blue for d in g.draws)
        )
        
    s = iter(games)
    s = map(minbag, s)
    s = map(lambda d: d.red * d.blue * d.green, s)
    power_sum = sum(s)
    
    print('power sum', power_sum)
        
    
def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***')

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
    