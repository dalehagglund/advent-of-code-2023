from camel import *
import pytest

ordering_tests = [
    ("2", "2", 0),
    ("2", "3", -1),
    ("3", "2", +1),  
]
@pytest.mark.parametrize("c1,c2,expected", ordering_tests)
def test_card_ordering(c1, c2, expected):
    assert cmp_card(c1, c2) == expected
