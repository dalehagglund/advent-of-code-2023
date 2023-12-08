from collections import Counter
from dataclasses import dataclass
from functools import total_ordering

CARDS = "23456789TJQKA"
_CARD_ORDER = { card: pos for pos, card in enumerate(CARDS) }

def cmp_card(c1: str, c2: str) -> int:
    delta = _CARD_ORDER[c1] - _CARD_ORDER[c2]
    if delta < 0: return -1
    if delta > 0: return +1
    return 0

@dataclass
class Hand:
    _cards: str
    _counts: Counter[str]
    _labels: set[str]
    _shape: tuple[int, int, int, int, int]

    def __init__(self, cards: str):
        assert len(cards) == 5
        self._cards: str = cards
        self._counts: Counter[str] = Counter(cards)
        self._labels: set[str] = set(cards)
        self._shape = tuple(sorted(map(lambda s: self._counts[s], self._labels)))

    def is_five_of_a_kind(self):
        return self._shape == (5,)
       
    def is_four_of_a_kind(self):
        return self._shape == (1, 4)
    
    def is_full_house(self):
        return self._shape == (2, 3)
        
    def is_three_of_a_kind(self):
        return self._shape == (1, 1, 3)
        
    def is_two_pair(self):
        return self._shape == (1, 2, 2)

    def is_one_pair(self):
        return self._shape == (1, 1, 1, 2)
        
    def is_high_card(self):
        return self._shape == (1, 1, 1, 1, 1)
        
    def __eq__(self, other) -> bool:
        if self is other: return True
        if self._counts != other._counts: return False
        return self._cards == other._cards
        
    def __lt__(self, other) -> bool:
        if self is other: return False
        