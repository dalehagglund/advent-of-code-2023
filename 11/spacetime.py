from tools import *
from enum import Enum, auto
import typing as ty
import operator
from dataclasses import dataclass, field
from functools import partial
from itertools import pairwise
import re

class Dir(tuple, Enum):
    L = ( 0, -1)
    R = ( 0, +1)
    U = (-1,  0)
    D = (+1,  0)

class Point(ty.NamedTuple):
    row: int
    col: int
    
    def manhattan_dist(self, other: ty.Self) -> int:
        return abs(other.row - self.row) + abs(other.col - self.col)
    
    def __add__(self, other: ty.Self) -> ty.Self:
        return Point(*map(operator.add, self, other))

@dataclass
class Universe:
    _grid: list[list[str]]
    
    def nrow(self):
        return len(self._grid)
    def ncol(self):
        return len(self._grid[0])

    def at(self, place: Point) -> str:
        r, c = place
        return self._grid[r][c]
    def row(self, r: int) -> str:
        assert 0 <= r < self.nrow()
        return self._grid[r]
    def col(self, c: int) -> str:
        assert 0 <= c < self.ncol()
        return ''.join(
            self._grid[r][c]
            for r 
            in range(self.nrow())
        )
        
    def is_valid(self, pos: Point) -> bool:
        r, c = pos
        if not (0 <= r < self.nrow()): return False
        if not (0 <= c < self.ncol()): return False
        return True

    def neighbours(self, pos: Point) -> ty.Iterator[Point]:
        for dir in (Dir.L, Dir.R, Dir.U, Dir.D):
            newpos = pos + dir
            if not self.is_valid(newpos):
                continue
            yield newpos
        
    def expand_empty_rows(self):
        new_grid = []
        for r in range(self.nrow()):
            new_grid.append(self._grid[r])
            if re.match(r"^\.*$", self.row(r)):
                new_grid.append(self._grid[r])
        self._grid = new_grid

    def expand_empty_cols(self):
        def transpose(grid: list[str]) -> list[str]:
            nr, nc = len(grid), len(grid[0])
            new = []
            for c in range(nc):
                new.append(''.join(grid[r][c] for r in range(nr)))
            return new
            
        self._grid = transpose(self._grid)
        self.expand_empty_rows()
        self._grid = transpose(self._grid)

    @classmethod
    def from_lines(cls, input: list[str]) -> ty.Self:
        assert all(len(l1) == len(l2) for l1, l2 in pairwise(input))
        return cls(_grid=input)
        