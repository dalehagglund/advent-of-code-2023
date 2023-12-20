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
    
def make_parts(xrange, default=range(5)) -> PartRange:
    return PartRange(x=xrange, m=default, a=default, s=default)

def test_partrange_splitting_fails_on_empty_interval():
    part = make_parts(range(50, 50))
    rule = Rule.from_str("x<10:xyzzy")
    with pytest.raises(AssertionError):
        _ = rule.split_parts(part)

def is_unchanged(orig, new, fields: str) -> bool:
    orig = dataclasses.asdict(orig)
    new = dataclasses.asdict(new)
    return all(orig[f] == new[f] for f in fields)

def abuts(r1, r2) -> bool:
    return r1.stop == r2.start or r2.stop == r1.start

@pytest.mark.parametrize(
    "lo,hi,op,cut",
    [
        (50, 60, "<", 49),
        (50, 60, "<", 50),
        (50, 60, "<", 51),
        (50, 60, "<", 55),
        (50, 60, "<", 59),
        (50, 60, "<", 60),
        (50, 60, "<", 61),
        
        (50, 51, "<", 49),
        (50, 51, "<", 50),
        (50, 51, "<", 51),
        (50, 51, "<", 52),

        (50, 60, ">", 49),
        (50, 60, ">", 50),
        (50, 60, ">", 51),
        (50, 60, ">", 55),
        (50, 60, ">", 59),
        (50, 60, ">", 60),
        (50, 60, ">", 61),

        (50, 51, ">", 50),
        (50, 51, ">", 51),
        (50, 51, ">", 51),
        (50, 51, ">", 52),
    ]
)
def test_partrange_splitting(lo, hi, op, cut):
    xrange = range(lo, hi)
    parts = make_parts(xrange)
    rule = Rule.from_str(f"x{op}{cut}:xyzzy")
    
    t, f = rule.split_parts(parts)

    assert is_unchanged(parts, t, "mas")
    assert is_unchanged(parts, f, "mas")
    
    assert min(t.x.start, f.x.start) == xrange.start
    assert max(t.x.stop, f.x.stop) == xrange.stop
    
    assert len(t.x) + len(f.x) == len(parts.x)
    assert abuts(t.x, f.x)
    
    for n in xrange:
        result = rule._predicate(Part(x=n))
        if result: assert n in t.x
        else:      assert n in f.x

#
# we don't need to test the "true" predicates with just a string, since
# they're always in the last position of a flow, and the Rule.split_parts()
# method is never invoked on the final position.
#
# def test_partrange_splitting_with_terminal_rule():
    # xrange = range(50, 60)
    # parts = make_parts(xrange)
    # rule = Rule.from_str(f"xyzzy")
    
    # t, f = rule.split_parts(parts)
