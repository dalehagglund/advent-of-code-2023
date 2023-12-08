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

@pytest.mark.parametrize(
    "cards, expected", [
        ("AAAAA", False),
        ("22224", False),
        ("22233", False),
        ("77889", False),
        ("22345", True),
        ("23452", True),
    ]
)
def test_one_pair(cards, expected):
    hand = Hand(cards)
    assert hand.is_one_pair() == expected
    
@pytest.mark.parametrize(
    "cards, expected", [
        ("AAAAA", False),
        ("22224", False),
        ("22233", False),
        ("77889", False),
        ("22345", False),
        ("23456", True),
        ("AKQJT", True),
    ]
)
def test_one_pair(cards, expected):
    hand = Hand(cards)
    assert hand.is_high_card() == expected
    
@pytest.mark.parametrize(
    "h1,h2,expected", [
        ("AAAAA", "AAAAA", True),
        ("AAAA2", "AAAA3", False),
        ("AAAA2", "2AAAA", False),
    ]
)
def test_hand_equality(h1, h2, expected):
    assert (Hand(h1) == Hand(h2)) == expected

@pytest.mark.parametrize(
    "cards1,cards2,expected", [
        ("23456", "2K456", True),
        ("2K456", "23456", False),
        ("23245", "2K245", True),
        ("T5T44", "55344", False),
        ("33344", "44333", True),
        ("44333", "33344", False),
    ]
)
def test_less_than_same_shape(cards1, cards2, expected):
    h1, h2 = Hand(cards1), Hand(cards2)
    assert h1._shape == h2._shape
    assert (h1 < h2) == expected

@pytest.mark.parametrize(
    "cards1,cards2,expected", [
        ("45678", "22456", True),
        ("22456", "22336", True),
        ("22336", "12333", True),
        ("22256", "22233", True),
        ("22233", "22226", True),
        ("22226", "22222", True),
    ]
)
def test_hand_less_than_different_shapes(cards1, cards2, expected):
    h1, h2 = Hand(cards1), Hand(cards2)
    assert h1._shape != h2._shape
    assert (h1 < h2) == expected
    assert (h1 > h2) == (not expected)
