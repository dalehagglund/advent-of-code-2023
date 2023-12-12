from tools import *
from enum import Enum, auto
import typing as ty
import operator
from dataclasses import dataclass, field
from functools import partial
from itertools import pairwise
import re

class Point(ty.NamedTuple):
    row: int
    col: int
    
    def manhattan_dist(self, other: ty.Self) -> int:
        return abs(other.row - self.row) + abs(other.col - self.col)
    
    def __add__(self, other: ty.Self) -> ty.Self:
        return Point(*map(operator.add, self, other))

@dataclass
class Universe:
    _galaxies: list[Point]  # *original* positions
    _rowshift: list[int]  # translate original rows to expanded rows
    _colshift: list[int]  # ditto for columns

    def expand(self, scale: int = 1):
        if scale == 1:
            return

        occupied_rows = { r for r, _ in self._galaxies }
        occupied_cols = { c for _, c in self._galaxies }
        nrows = len(self._rowshift)
        ncols = len(self._colshift)
        
        rowshift = list(
            itertools.accumulate(
                (scale - 1) if r not in occupied_rows else 0
                for r in range(nrows)
            )
        )
        
        colshift = list(
            itertools.accumulate(
                (scale - 1) if c not in occupied_cols else 0
                for c in range(ncols)
            )
        )

        self._rowshift, self._colshift = rowshift, colshift

    def galaxy_positions(self): 
        return [
            Point(r, c) + Point(self._rowshift[r] , self._colshift[c])
            for r, c
            in self._galaxies
        ]

    @classmethod
    def from_lines(cls, input: list[str]) -> ty.Self:
        assert all(len(l1) == len(l2) for l1, l2 in pairwise(input))
        nrow, ncol = len(input), len(input[0])
        galaxies = [
            Point(r, c)
            for r, c in 
            product(nrow, ncol)
            if input[r][c] == '#'
        ]
        
        return cls(
            _galaxies=galaxies, _rowshift=[0]*nrow, _colshift=[0]*ncol
        )
        