import collections
import operator
import functools
import itertools
import typing as ty

#
# general tools for iterables, mapping, etc.
#

def star(f):
    return lambda t: f(*t)

def ident(x): return x

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

def product(*ranges, repeat=1):
    ranges = (
        range(r) if isinstance(r, int) else r
        for r in ranges
    )
    return itertools.product(*ranges, repeat=repeat)

def nth(n, items): return items[n]
def mul(items): return functools.reduce(operator.mul, items, 1)

# in a streamy sequence of generators, this might be useful to 
# describe a sequence of operations to be applied to each item
# of the an iterable.
def seq(*funcs):
    def _inner(arg):
        for f in funcs:
            arg = f(arg)
        return arg
    return _inner
    
#
# some routines for helping with input
#

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

def convert_ints(items: list[str]) -> list:
    return [
        int(item) if re.match("^[0-9]*$", item) else item
        for item in items
    ]
            