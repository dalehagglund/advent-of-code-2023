from camel import *
import pytest

ordering_tests = [
]
@pytest.mark.parametrize(
    "c1,c2,expected", [
        ("2", "2", 0),
        ("2", "3", -1),
        ("3", "2", +1),  
    ]
)
def test_card_ordering(c1, c2, expected):
    assert cmp_card(c1, c2) == expected

def test_hand_counts():
    h = Hand("22333")
    assert h._counts["2"] == 2
    assert h._counts["3"] == 3

@pytest.mark.parametrize(
    "cards,expected", [
        ("AAAAA", True),
        ("AAAAK", False),
        ("2346T", False),
        ("QQQQQ", True),
    ]
)        
def test_five_of_a_kind(cards, expected):
    h = Hand(cards)
    assert h.is_five_of_a_kind() == expected
    
@pytest.mark.parametrize(
    "cards, expected", [
        ("AAAAA", False),
        ("22233", False),
        ("2222A", True),
    ]
)
def test_four_of_a_kind(cards, expected):
    hand = Hand(cards)
    assert hand.is_four_of_a_kind() == expected


@pytest.mark.parametrize(
    "cards, expected", [
        ("AAAAA", False),
        ("22334", False),
        ("777AA", True),
        ("77AA7", True),
    ]
)
def test_full_house(cards, expected):
    hand = Hand(cards)
    assert hand.is_full_house() == expected
    
@pytest.mark.parametrize(
    "cards, expected", [
        ("AAAAA", False),
        ("22334", False),
        ("777AK", True),
        ("77JK7", True),
    ]
)
def test_three_of_a_kind(cards, expected):
    hand = Hand(cards)
    assert hand.is_three_of_a_kind() == expected

@pytest.mark.parametrize(
    "cards, expected", [
        ("AAAAA", False),
        ("22224", False),
        ("22233", False),
        ("77889", True),
        ("TJTJQ", True),
    ]
)
def test_two_pair(cards, expected):
    hand = Hand(cards)
    assert hand.is_two_pair() == expected
