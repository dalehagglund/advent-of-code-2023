# tests for the camel game with jokers wild

from camel import *
import pytest
from functools import partial

make_hand = partial(Hand, wild=True)

def test_ordinary_hands_have_correct_category():
    assert make_hand("23456").is_high_card()
    assert make_hand("22456").is_one_pair()
    assert make_hand("22446").is_two_pair()
    assert make_hand("22256").is_three_of_a_kind()
    assert make_hand("22255").is_full_house()
    assert make_hand("22226").is_four_of_a_kind()
    assert make_hand("22222").is_five_of_a_kind()

@pytest.mark.parametrize(
    "cards", [ "22222", "JJJJJ" ]
)
def test_upgrade_five_of_a_kind(cards):
    assert make_hand(cards).is_five_of_a_kind()

@pytest.mark.parametrize(
    "cards,test", [
        # from 4 of a kind
        ("2222J", Hand.is_five_of_a_kind), 
        ("JJJJ3", Hand.is_five_of_a_kind),
        # from full house
        ("222JJ", Hand.is_five_of_a_kind),
        ("JJJ22", Hand.is_five_of_a_kind),
        # from 3 of a kind
        ("222JK", Hand.is_four_of_a_kind),
        ("JJJ23", Hand.is_four_of_a_kind),
        # from 2 pair
        ("2233J", Hand.is_full_house),
        ("22JJ5", Hand.is_four_of_a_kind),
        # from 1 pair
        ("22JQK", Hand.is_three_of_a_kind),
        ("JJ234", Hand.is_three_of_a_kind),
        # from high card
        ("J2345", Hand.is_one_pair),
    ]
)
def test_upgrades(cards, test):
    assert test(make_hand(cards))
