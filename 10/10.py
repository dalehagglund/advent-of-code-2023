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
        
    def one(collection):
        assert len(collection) == 1
        return next(iter(collection))
    
    def is_vertex(node):
        at = graph.at(node)
        if at in "LJ7F": return True
        if at in "-|": return False
        assert at == "S"
        n1, n2 = graph.neighbours(node)
        if n1[0] == n2[0] or n1[1] == n2[1]: return False
        return True
        
    
    def find_vertices(curve, start):
        import random
        
        node  = start
        prevnode = None
        startcount = 0
        
        while True:
            assert node in curve
            if is_vertex(node):
                yield node
            if node == start: startcount += 1
            if node == start and startcount == 2:
                break
            neighbours = set(graph.neighbours(node))
            if prevnode is None:
                prevnode, node = (
                    node,
                    neighbours.pop()
                )
            else:
                prevnode, node = (
                    node, 
                    one(neighbours - {prevnode})
                )
                
    
    def area(vertices):
        # via the trapezoid form of the Shoelace Formula, 
        # and assuming vertices[-1] == vertices[0]
        return abs(sum(
            (y2 + y1) * (x1 - x2)
            for (y1, x1), (y2, x2)
            in itertools.pairwise(vertices)
        )) / 2

    vertices = list(find_vertices(curve, start))
    
    # use Pick's Theorem, which says that for a simple polygone with 
    # integer coordinates
    #
    #    A = I + B/2 - 1
    #
    # where A is the area, I is the number of lattice points inside
    # the polgon, and B is the number of lattice points on the boundary.
    #
    # Solving for IO
    #
    #    I = A - B/2 + 1
    #
    
    B = len(curve)
    A = area(vertices)

    print(f'{(A, B) = }')
    return A - B//2 + 1
        

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
