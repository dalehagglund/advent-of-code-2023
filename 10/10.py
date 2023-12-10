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
from grid import *

def find_interior_size(graph, start):
    curve = set()

    queue = collections.deque()
    queue.append(start)
    while len(queue) > 0:
        label = queue.popleft()
        if label in curve:
            continue
        curve.add(label)
        queue.extend(
            neighbour
            for neighbour
            in graph.neighbours(label)
        )

    def extend(point):
        assert point in graph._graph
        assert point not in curve
        r, c = point
        while (r, c) in graph._graph:
            yield (r, c)
            r += 1

    def crossings(point):
        ray = collections.deque(extend(point))
        segments = []
        
        def followed_by(p1, p2):
            return p1 in graph._graph[p2]._adjacent

        while ray:
            while ray and graph.at(ray[0]) == ".":
                ray.popleft()
            if not ray:
                break
            seg = [ray.popleft()]
            while ray and followed_by(seg[-1], ray[0]):
                seg.append(ray.popleft())
            segments.append(seg)
            
        n = sum(
            2 if len(seg) >= 2 else 1
            for seg 
            in segments
        )
        if (
            segments and
            len(segments[-1]) > 1 and
            segments[-1][-1][0]  == graph._nrow - 1
        ):
            print("!adjust")
            n += 1
        print(f'crossings({point}) - {n}: {segments = }')
        return n

    interior = set()
    exterior = set()
    
    for point in graph.labels():
        if point in curve: continue
        if crossings(point) % 2 == 0:
            exterior.add(point)
        else:
            interior.add(point)
  
    return len(interior)

def find_max_depth(graph, start):
    max_depth = float('-inf')
    seen = set()
    queue = collections.deque()
    queue.append((start, 0))
    while len(queue) > 0:
        label, depth = queue.popleft()
        if label in seen:
            continue
        seen.add(label)
        max_depth = max(max_depth, depth)
        queue.extend(
            (neighbour, depth + 1)
            for neighbour
            in graph.neighbours(label)
        )
        
    return max_depth

def solve1(sections: list[list[str]]) -> int:
    grid = Grid.from_map(sections[0])
    return find_max_depth(grid, grid.start())

def solve2(sections: list[list[str]]) -> int:
    grid = Grid.from_map(sections[0])
    return find_interior_size(grid, grid.start())

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
