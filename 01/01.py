import sys
import typing as ty
from dataclasses import dataclass, field
from enum import Enum
import functools
from functools import partial
import collections
import re
import itertools
from itertools import (
    islice,
    product,
    pairwise,
    zip_longest
)
import abc
from functools import reduce, cmp_to_key
import operator
import collections
from copy import deepcopy
import unittest

def star(f):
    return lambda t: f(*t)

def splitby(predicate, items):
    batch = []
    for item in items:
        if predicate(item):
            yield batch
            batch = []
            continue
        else:
            batch.append(item)
    if batch:
        yield batch
        
def chunked(items, n):
    iters = [ iter(items) ] * n
    return zip(*iters, strict=True)

def sliding_window(items, n):
    window = collections.deque(maxsize=n)
    window.extend(islice(items, n))
    if len(window) == n:
        yield tuple(window)
    for item in items:
        window.append(item)
        yield tuple(window)
    
def trim_newline(line: str) -> str:
    return line[:-1] if line[-1] == '\n' else line
        
def read_sections(file, trim=True) -> list[list[str]]:
    s = iter(file)
    s = map(trim_newline, s)
    s = map(str.rstrip if trim else ident, s)
    s = splitby(lambda line: line == '', s)
    return list(s)
    
def convert_fields(funcs, items: ty.Sequence[ty.Any]):
    return tuple(
        f(item)
        for f, item
        in zip(funcs, items)
        if f is not None
    )

def ident(x): return x
    
def observe(func, items):
    for item in items:
        func(item)
        yield item

def drain(iterable):
    for s in iterable:
        pass

def collect(factory, iterable):
    return factory(iterable)
    
def takeuntil(predicate, items):
    for item in items:
        yield item
        if predicate(item):
            break

def sign(n: int) -> int:
    if   n < 0: return -1
    elif n > 0: return +1
    else:       return 0

def convert_ints(items: list[str]) -> list:
    return [
        int(item) if re.match("^[0-9]*$", item) else item
        for item in items
    ]
    
def product(*ranges, repeat=1):
    ranges = (
        range(r) if isinstance(r, int) else r
        for r in ranges
    )
    return itertools.product(*ranges, repeat=repeat)

def nth(n, items): return items[n]
def mul(items): reduce(operator.mul, items, 1)
def seq(*funcs):
    def _inner(arg):
        for f in funcs:
            arg = f(arg)
        return arg
    return _inner
def compose(*funcs):
    return seq(funcs[::-1])

# map(seq(partial(map, f), list), ...)
# map(compose(list, partial(map, f)), ...)
# s = map(partial(map, f), ...); s = map(list, s)
# map(lambda item: list(map(f, item)), ...)
def mapinner(f, items):
    for item in items:
        yield list(map(f, item))

def find_simple_digit(s:str) -> str:
    for c in s:
        if c in "0123456789":
            return c

def part1(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 1 ***')
    
    total = 0
    for line in sections[0]:
        d1 = find_simple_digit(line)
        d2 = find_simple_digit(line[::-1])
        calibration = int(d1 + d2)
        total += calibration
    print(total)

def find_complex_digit(s: str) -> tuple[str, str]:
    pattern = r'''one|two|three|four|five|six|seven|eight|nine|[0123456789]'''
    to_fwd_digit = {}
    to_rev_digit = {}
    
    for i in range(10):
        to_fwd_digit[str(i)] = str(i)
        to_rev_digit[str(i)] = str(i)
    for i, name in zip(
        itertools.count(0),
        ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    ): 
        to_fwd_digit[name] = str(i)
        to_rev_digit[name[::-1]] = str(i)
    
    fwd_pattern = '|'.join(to_fwd_digit.keys())
    rev_pattern = '|'.join(to_rev_digit.keys())    
    
    fwd_matches = re.findall(fwd_pattern, s)
    rev_matches = re.findall(rev_pattern, s[::-1])
    return to_fwd_digit[fwd_matches[0]], to_rev_digit[rev_matches[0]]

def part2(fname: str):
    with open(fname) as f:
        sections = read_sections(f)
    print(f'*** part 2 ***')
    total = 0
    for line in sections[0]:
        d1, d2 = find_complex_digit(line)
        calibration = int(d1 + d2)
        print(calibration, line)
        total += calibration
    print(total)

if __name__ == '__main__':
#    part1(sys.argv[1])
    part2(sys.argv[1])
    