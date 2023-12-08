from collections import Counter
from dataclasses import dataclass
from functools import total_ordering

_STANDARD_CARD_ORDER = {
    card: pos for pos, card in enumerate("23456789TJQKA")
}

_JOKERS_WILD_CARD_ORDER = {
    card: pos for pos, card in enumerate("J23456789TQKA")
}

def card_pos(c: str) -> int:
    assert len(c) == 1
    return _STANDARD_CARD_ORDER[c]

@total_ordering
@dataclass
class Hand:
    _cards: str
    _counts: Counter[str]
    _shape: tuple[int, int, int, int, int]
    
    _SHAPE_RANK = {
        (1, 1, 1, 1, 1): 0,
        (1, 1, 1, 2): 1,
        (1, 2, 2): 2,
        (1, 1, 3): 3,
        (2, 3): 4,
        (1, 4): 5,
        (5,): 6,
    }

    def __init__(self, cards: str, wild=False):
        assert len(cards) == 5
        self._cards: str = cards
        self._counts: Counter[str] = Counter(cards)
        self._shape = tuple(sorted(map(lambda s: self._counts[s], set(cards))))     
        if wild:
            self._upgrade_hand(self._counts)
            
    def _upgrade_hand(self, counts):
        jcount = counts["J"]
        if jcount == 0:
            return
        
        if self._shape == (5,): 
            pass
        elif self._shape == (1, 4) and jcount in (1, 4):
            self._shape = (5,)
        elif self._shape == (2, 3) and jcount in (2, 3):
            self._shape = (5,)
        elif self._shape == (1, 1, 3) and jcount in (1, 3):
            self._shape = (1, 4)
        elif self._shape == (1, 2, 2) and jcount == 1:
            self._shape = (2, 3)
        elif self._shape == (1, 2, 2) and jcount == 2:
            self._shape = (1, 4)
        elif self._shape == (1, 1, 1, 2) and jcount in (1, 2):
            self._shape = (1, 1, 3)
        elif self._shape == (1, 1, 1, 1, 1) and jcount == 1:
            self._shape = (1, 1, 1, 2)
        else:
            raise AssertionError(
                f'no upgrade applies: {self._shape = } {jcount = }'
            )

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
        if self._shape != other._shape: return False
        return self._cards == other._cards
        
    def __lt__(self, other) -> bool:
        if self is other:
            return False
        if self._shape != other._shape:
            return self._SHAPE_RANK[self._shape] < self._SHAPE_RANK[other._shape]        
        return tuple(map(card_pos, self._cards)) < tuple(map(card_pos, other._cards))