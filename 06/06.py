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

def read_input_tuples(sec: list[str], part2=False) -> list[tuple[int, int]]:
    times = sec[0].split()[1:]
    distances = sec[1].split()[1:]
    
    if not part2:    
        return list(
            zip(
                map(int, times),
                map(int, distances)
            )
        )
        
    time = int(''.join(times))
    distance = int(''.join(distances))
    return [ (time, distance) ]

def dist(h: int, M: int) -> int:
    assert h <= M
    return (M - h)*h

def solve1(sec: list[str]) -> int:
    games = read_input_tuples(sec)
    product = 1
    
    for g in games:
        M, record = g
        print(f'> {M = } {record = }')
        for h in range(0, M+1):
            print(f'   > {h = } {dist(h, M) = }')
            if dist(h, M) > record:
                wins = (M - h) - h + 1
                print(f'   > {wins = }')
                product *= wins
                break
    return product
    
def solve2(sec: list[str]) -> int:
    games = read_input_tuples(sec, part2=True)
    product = 1
    for g in games:
        M, record = g
        print(f'> {M = } {record = }')
        for h in range(0, M+1):
            print(f'   > {h = } {dist(h, M) = }')
            if dist(h, M) > record:
                wins = (M - h) - h + 1
                print(f'   > {wins = }')
                product *= wins
                break

    return product

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***', solve1(sections[0]))
    
def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve2(sections[0]))

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
