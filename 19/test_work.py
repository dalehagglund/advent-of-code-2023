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
    assert rule.eval(part) == "xyzzy"
    
def test_conditional_rule():
    part = Part.from_str("{x=1,m=2,a=3,s=4}")
    
    truerule  = Rule.from_str("x<3:less")
    falserule = Rule.from_str("x>1:greater") 
    assert truerule.eval(part) == "less"
    assert falserule.eval(part) == None
    
def test_workflow_name():
    flow = Flow.from_str("a{R}")
    assert flow.name() == "a"

def test_workflow():
    flow = Flow.from_str("a{x>3:foo,bar}")
    failpart = Part(x=3)
    truepart = Part(x=4)
    
    assert flow.eval(failpart) == "bar"
    assert flow.eval(truepart) == "foo"