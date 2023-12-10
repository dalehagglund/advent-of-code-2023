import typing as ty
from dataclasses import dataclass, field
from tools import *
from enum import Enum, auto
from functools import partial

Label = tuple[int, int]

class Dir:
    L = ( 0, -1)
    R = ( 0, +1)
    U = (-1, 0 )
    D = (+1, 0 )

@dataclass
class Node:
    _label: Label
    _adjacent: set[Label] = field(default_factory=set)

_connections = {
    "|": {Dir.U, Dir.D},
    "-": {Dir.L, Dir.R},
    
    "L": {Dir.R, Dir.U},
    "J": {Dir.L, Dir.U},
    "7": {Dir.L, Dir.D},
    "F": {Dir.R, Dir.D},
    
    ".": {},
}

@dataclass
class Grid:
    _nrow: int
    _ncol: int
    _start: Label
    _graph: dict[Label, Node]
    
    def start(self):
        return self._start
    def neighbours(self, label):
        return iter(self._graph[label]._adjacent)

    @classmethod
    def from_map(cls, lines) -> ty.Self:
        nrow = len(lines)
        ncol = len(lines[0])

        def at(lab: Label):
            r, c = lab
            return lines[r][c]
        def adjust(lab: Label, dr, dc): 
            r, c = lab
            return (r + dr, c + dc)
        def possible_neighbours(here: Label):
            s = _connections[at(here)]
            s = map(star(partial(adjust, here)), s)
            s = filter(lambda pos: pos in graph, s)
            s = filter(lambda pos: at(pos) != ".", s)
            return s
        def can_connect(here, there) -> bool:
            if at(there) == ".": return
        graph = {
            (r, c): Node((r, c))
            for r, c
            in product(nrow, ncol)
        }
        
        start = None

        # record "outbound" adjacencies from each map cell

        for pos, node in graph.items():
            sym = at(pos)
            if sym == "S":
                start = pos
                continue
            for neighbour in possible_neighbours(pos):
                graph[pos]._adjacent.add(neighbour)

        assert start != None
        
        # find the adjacencies for the start node

        for dr, dc in [ Dir.U, Dir.D, Dir.L, Dir.R ]:
            neighbour = adjust(start, dr, dc)
            if neighbour not in graph: continue
            if start in graph[neighbour]._adjacent:
                graph[start]._adjacent.add(neighbour)

        assert len(graph[start]._adjacent) == 2
        
        # prune outbound adjacencies that are dead ends

        for pos, node in graph.items():
            to_remove = set(
                adj
                for adj 
                in node._adjacent
                if pos not in graph[adj]._adjacent
            )
            node._adjacent -= to_remove

        # make sure each edge goes both ways

        for pos, node in graph.items():
            for adj in node._adjacent:
                graph[adj]._adjacent.add(pos)

        return cls(nrow, ncol, start, graph)
