from collections import Counter

CARDS = "23456789TJQKA"
_CARD_ORDER = { card: pos for pos, card in enumerate(CARDS) }

def cmp_card(c1: str, c2: str) -> int:
    delta = _CARD_ORDER[c1] - _CARD_ORDER[c2]
    if delta < 0: return -1
    if delta > 0: return +1
    return 0
    
class Hand:
    def __init__(self, cards: str):
        assert len(cards) == 5
        self._cards: str = cards
        self._counts: Counter[str] = Counter(cards)
        self._labels: set[str] = set(cards)

    def is_five_of_a_kind(self):
        if len(self._counts) > 1: return False
        label = next(iter(self._counts.keys()))
        assert self._counts[label] == 5
        return True
        
    def is_four_of_a_kind(self):
        if len(self._labels) > 2: return False
        counts = sorted(map(lambda s: self._counts[s], self._labels))
        return counts == [1, 4]
    
    def is_full_house(self):
        if len(self._labels) > 2: return False
        counts = sorted(map(lambda s: self._counts[s], self._labels))
        return counts == [2, 3]
        
    def is_three_of_a_kind(self):
        counts = sorted(map(lambda s: self._counts[s], self._labels))
        return counts == [1, 1, 3]
        
    def is_two_pair(self):
        counts = sorted(map(lambda s: self._counts[s], self._labels))
        return counts == [1, 2, 2]

