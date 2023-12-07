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