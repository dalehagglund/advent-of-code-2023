import pytest

from tools import *

def test_star():
    def f(a, b, c):
        assert a == 1
        assert b == 2
        assert c == 3
    star(f)((1, 2, 3))

def test_splitby_empty_sequence():
    def predicate(item):
        raise Exception("shouldn't be called on empty list")
    batches = list(splitby(predicate, []))
    assert len(batches) == 0
    
def test_splitby_initial_match():
    batches = list(splitby(lambda item: item == -1, [-1, 2, 3]))
    assert len(batches) == 2
    assert len(batches[0]) == 0
    assert batches[1] == [2, 3]
    
def test_splitby_middle_match():
    batches = list(splitby(lambda item: item == -1, [1, 2, -1, 3, 4]))
    assert len(batches) == 2
    assert batches[0] == [1, 2]
    assert batches[1] == [3, 4]
    
def test_chunked_full_last_chunk():
    chunks = list(chunked([1, 2, 3, 4], 2))
    assert len(chunks) == 2
    assert chunks[0] == (1, 2)
    assert chunks[1] == (3, 4)
    
def test_chunked_partial_last_batch_fails():
    with pytest.raises(ValueError):
        list(chunked([1, 2, 3, 4], 3))

def test_observe():
    observations = []    
    def observer(item):
        observations.append(item + 1)
    output = list(observe(observer, range(3)))
    assert output == [0, 1, 2]
    assert observations == [1, 2, 3]
    
def test_drain():
    items = iter([1, 2, 3])
    drain(items)
    with pytest.raises(StopIteration):
        next(items)

def test_collect():
    assert 6 == collect(sum, iter([1, 2, 3]))

def test_takeuntil_empty_list():
    def pred(item):
        raise Exception("unexpected call to predicate")
    assert [] == list(takeuntil(lambda item: False, []))

def test_takeuntil_false_predicate():
    def false(item): return False
    assert [1, 2, 3] == list(takeuntil(false, [1, 2, 3]))

def test_takeuntil_middle():
    items = iter([1, 2, 3])
    results = list(takeuntil(lambda item: item == 2, items))
    assert results == [1, 2]
    assert next(items) == 3
    
def test_product():
    output = list(product(2, range(3)))
    assert len(output) == 6
    assert output == [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
    ]

def test_seq():
    items = iter(range(5))
    output = list(map(seq(lambda n: n + 1, lambda n: n * 2), items))
    assert output == [
        2,
        4,
        6,
        8,
        10,
    ]