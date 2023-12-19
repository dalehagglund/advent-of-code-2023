import pytest
from work import *

def test_part():
    part = Part.from_str("{x=1,m=2,a=3,s=4}")
    assert part.x == 1
    assert part.m == 2
    assert part.a == 3
    assert part.s == 4
    
def test_default_rule():
    part = Part()
    rule = Rule.from_str("xyzzy")
    assert rule.out() == "xyzzy"
    assert rule.eval(part) == "xyzzy"
    
def test_conditional_rule():
    part = Part.from_str("{x=1,m=2,a=3,s=4}")
    
    truerule  = Rule.from_str("x<3:less")
    falserule = Rule.from_str("x>1:greater")
    
    assert truerule.eval(part) == "less"
    assert truerule.out() == "less"
    
    assert falserule.eval(part) == None
    assert falserule.out() == "greater"

def test_workflow_name():
    flow = Flow.from_str("a{R}")
    assert flow.name() == "a"

def test_workflow():
    flow = Flow.from_str("a{x>3:foo,bar}")
    failpart = Part(x=3)
    truepart = Part(x=4)
    assert flow.out() == { "foo", "bar" }
    assert flow.eval(failpart) == "bar"
    assert flow.eval(truepart) == "foo"
    
def test_partrange_size():
    p = PartRange(range(10), range(10), range(10), range(10))
    assert p.size() == 10**4
    
def test_partrange_splitting_():
    xrange = range(50, 60)
    parts = PartRange(x=xrange, m=range(5), a=range(5), s=range(5))
    rule = Rule.from_str("x<55:xyzzy")
    
    t, f = rule._predicate.splitparts(parts)

    assert t.m == t.a == t.s == range(5)
    assert f.m == f.a == f.s == range(5)
    assert t.x != f.x
    
    assert min(t.x.start, f.x.start) == xrange.start
    assert max(t.x.stop, f.x.stop) == xrange.stop
    
    assert t.x.stop == f.x.start or f.x.stop == t.x.start
    
    assert sum(rule._predicate(Part(x=n)) for n in t.x) == len(t.x)
    assert sum(rule._predicate(Part(x=n)) for n in f.x) == 0
