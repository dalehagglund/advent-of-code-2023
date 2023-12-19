import typing as ty
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
class Rule:
    _predicate: ty.Callable[[Part], bool]
    _flow: str

    def flow(self): return self._flow

    def eval(self, p: Part) -> ty.Optional[str]:
        return self._flow if self._predicate(p) else None

    @classmethod
    def from_str(cls, rulespec: str) -> ty.Self:
        # eg, "a>2000:foo"
        optab = {
            '<': operator.lt,
            '>': operator.gt,
        }
        
        if ":" in rulespec:
            pred, flow = rulespec.split(":")
            field, op, const = re.split(r'([<>])', pred)
            predicate = lambda p: (
                optab[op](getattr(p, field), int(const))
            )
        else:
            flow = rulespec
            predicate = lambda p: True
            
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

    @classmethod
    def from_str(cls, flowspec: str) -> ty.Self:
        name, rulespecs = re.split(r"[{}]", flowspec)[:-1]
        rules = list(map(Rule.from_str, rulespecs.split(",")))
        return Flow(_name=name, _rules=rules)