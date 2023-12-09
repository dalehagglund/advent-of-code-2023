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
import numpy as np
from pprint import pprint

from tools import *

def differences(vec: list[int]) -> list[int]:
    return [ n2 - n1 for n1, n2 in pairwise(vec) ]

def extrapolate_forward(vec: list[int]) -> int:
    if all(n == 0 for n in vec): return 0
    return vec[-1] + extrapolate_forward(differences(vec))

def extrapolate_backward(vec: list[int]) -> int:
    if all(n == 0 for n in vec): return 0
    return vec[0] - extrapolate_backward(differences(vec))


def solve1(sections: list[list[str]]) -> int:
    s = iter(sections[0])
    s = map(str.split, s)
    s = map(partial(map, int), s)
    s = map(list, s)
    s = observe(partial(print, "#1 "), s)
    s = map(extrapolate_forward, s)
    s = observe(partial(print, "#2 "), s)
    return sum(s)

def solve2(sections: list[list[str]]) -> int:
    s = iter(sections[0])
    s = map(str.split, s)
    s = map(partial(map, int), s)
    s = map(list, s)
    s = observe(partial(print, "#1 "), s)
    s = map(extrapolate_backward, s)
    s = observe(partial(print, "#2 "), s)
    return sum(s)
    
def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***', solve1(sections))
    
def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve2(sections))

if __name__ == '__main__':
    part1(sys.argv[1])
    part2(sys.argv[1])
