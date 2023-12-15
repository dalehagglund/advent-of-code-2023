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
    lru_cache,
)
import numpy as np
from pprint import pprint
import contextlib
import time
import operator

from tools import *

def HASH(s: str) -> int:
    current = 0
    for code in map(ord, s):
        current += code
        current *= 17
        current %= 256
    return current

def solve1(sections: list[list[str]]) -> int:
    assert len(sections) == 1
    assert len(sections[0]) == 1
    line = sections[0][0]
    s = line.split(",")
    s = map(HASH, s)
    return sum(s)

def lens_pos(lens, box):
    for i, (label, _) in enumerate(box):
        if label == lens:
            return i
    return len(box)

def remove_lens(lens: str, box: list):
    index = lens_pos(lens, box)
    if index < len(box):
        box.pop(index)

def show_boxes(boxes, indent=0):
    prefix = " " * indent
    for i, box in enumerate(boxes):
        if len(box) == 0: continue
        print(f'{prefix}box {i}: {box}')

def box_power(b, box):
    power = 0
    for pos, (lens, focal_len) in enumerate(box):
        power += (b + 1) * (pos + 1) * focal_len
    return power

def solve2(sections: list[list[str]]) -> int:
    boxes: list[tuple[str, int]] = list([] for _ in range(255))
    line = sections[0][0]
    s = line.split(",")
    s = map(partial(re.split, r'([-=])'), s)
    for lens, op, arg in s:
        b = HASH(lens)
        if op == '-':
            remove_lens(lens, boxes[b])
        elif op == '=':
            focal = int(arg)
            box = boxes[b]
            pos = lens_pos(lens, box)
            if pos < len(box):
                box[pos] = (lens, focal)
            else:
                box.append((lens, focal))
        
    s = enumerate(boxes)
    s = map(star(box_power), s)
    return sum(s)

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***', solve1(sections))
    
def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***', solve2(sections))

def usage(message):
    prog = sys.argv[0]
    print(f'usage: {prog} [-1|-2] [--] input_file...')
    print(f'    {message}')
    sys.exit(1)

def main(args):
    infile = None
    run1 = run2 = False
    
    while args and args[0].startswith('-'):
        arg = args.pop(0)
        if arg in ('--'): break
        elif re.match(r'^-[A-Za-z0-9]{2,}$', arg):
            args[:0] = list(map(partial(operator.add, '-'), arg[1:]))
        elif arg in ('-1'): run1 = True
        elif arg in ('-2'): run2 = True
        else:
            usage(f'{arg}: unexpected option')

    if not (run1 or run2): run1 = run2 = True

    if len(args) == 0:
        usage("missing input file")
        
    if run1:
        for infile in args:
            part1(infile)

    if run2:
        for infile in args:
            part2(infile)
    
if __name__ == '__main__':
    main(sys.argv[1:])
