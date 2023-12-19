import typing as ty
import dataclasses
from dataclasses import dataclass, field
import functools
from functools import partial
import re
import operator

from tools import *

@dataclass(frozen=True)
class Part:
    x: int = 0
    m: int = 0
    a: int = 0
    s: int = 0
    
    @classmethod
    def from_str(cls, partspec: str) -> ty.Self:
        s = iter(partspec[1:-1].split(','))
        s = map(partial(str.split, sep="="), s)
        s = map(star(lambda name, val: (name, int(val))), s)
        kw = dict(s)
        return cls(**kw)
        
@dataclass(frozen=True)
class PartRange:
    x: range
    m: range
    a: range
    s: range
    
    def size(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)
                
@dataclass(frozen=True)
class Predicate:
    _left: str
    _op: str
    _right: int
    
    _OPTAB = {
        '<': operator.lt,
        '>': operator.gt,
    }

    def __call__(self, p: Part):
        return self._OPTAB[self._op](getattr(p, self._left), self._right)
    
    def split_parts(self, parts: PartRange) -> tuple[PartRange, PartRange]:
        field = self._left
        cut = self._right
        op = self._op

        interval = getattr(parts, field)
        assert len(interval) > 0

        def split(r: range, n):
            assert r.start <= n <= r.stop
            return range(r.start, n), range(n, r.stop)
        
        lo, hi = interval.start, interval.stop
        if cut < lo:
            if op == '<': t, f = split(interval, lo)
            else:         t, f = split(interval, hi)
        elif cut == lo:
            if op == '<': t, f = split(interval, lo)
            else:         t, f = reversed(split(interval, lo+1))
        elif lo < cut < hi:
            assert len(interval) > 1
            if op == '<': t, f = split(interval, cut)
            else:         t, f = reversed(split(interval, cut+1))
        elif hi == cut:
            if op == '<': t, f = split(interval, hi)
            else:         t, f = reversed(split(interval, hi))
        elif hi < cut:
            if op == '<': t, f = split(interval, hi)
            else:         t, f = split(interval, lo)
        else:
            assert False, f"shouldn't get here: {(op, cut, interval) = }"

        return (
            dataclasses.replace(parts, **{field: t}), 
            dataclasses.replace(parts, **{field: f})
        )

@dataclass(frozen=True)
class TruePredicate:
    def __call__(self, p: Part): return True

@dataclass(frozen=True)
class Rule:
    _predicate: ty.Callable[[Part], bool]
    _flow: str

    def out(self): return self._flow
    def split_parts(self, parts: PartRange) -> tuple[PartRange, PartRange]:
        return self._predicate.split_parts(parts)
    
    def eval(self, p: Part) -> ty.Optional[str]:
        return self._flow if self._predicate(p) else None

    @classmethod
    def from_str(cls, rulespec: str) -> ty.Self:
        # eg, "a>2000:foo" or "bar"
        
        if ":" in rulespec:
            pred, flow = rulespec.split(":")
            field, op, const = re.split(r'([<>])', pred)
            assert int(const) >= 1
            predicate = Predicate(field, op, int(const))
        else:
            flow = rulespec
            predicate = TruePredicate()
            
        return cls(
            _predicate = predicate,
            _flow = flow
        )
        
@dataclass(frozen=True)
class Flow:
    _name: str
    _rules: list[Rule]
    
    def name(self): return self._name
    def eval(self, p: Part) -> str:
        for r in self._rules:
            ruleval = r.eval(p)
            if ruleval is not None: break
        else:
            assert False, "fell off of rule chain"
        return ruleval
        
    def out(self):
        return set(r.out() for r in self._rules)

    @classmethod
    def from_str(cls, flowspec: str) -> ty.Self:
        name, rulespecs = re.split(r"[{}]", flowspec)[:-1]
        rules = list(map(Rule.from_str, rulespecs.split(",")))
        return Flow(_name=name, _rules=rules)