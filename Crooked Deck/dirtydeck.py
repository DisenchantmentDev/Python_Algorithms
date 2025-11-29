from playingcard import PlayingCard, CardSuit, _valid_rank_, _convert_to_rank
from collections.abc import Container
import unittest
import random


_full_deck_ = [PlayingCard(s, r) for s in CardSuit for r in range(1, 14)]


class DirtyDeck(Container):

    def __init__(self, *, hide=None):
        self.deck = _full_deck_.copy()
        self.hidden = None
        if hide is not None:
            if not _valid_rank_(hide):
                raise ValueError(f"{hide} is not a card rank")
            self.hidden = _convert_to_rank(hide)

    def __str__(self):
        retstr = ""
        for c in self.deck:
            retstr += f"{str(c)} "
        return retstr

    def __contains__(self, c):
        return c in self.deck

    def __len__(self):
        return len(self.deck)

    def __iter__(self):
        return iter(self.deck)

    def shuffle(self):
        self.deck = _full_deck_.copy()
        for i in range(len(_full_deck_) - 1, 0, -1):
            j = random.randint(0, i)
            if self.hidden is not None:
                if self.deck[j].rank == self.hidden:
                    self.deck.append(self.deck.pop(j))
                    continue
                elif self.deck[i].rank == self.hidden:
                    self.deck.append(self.deck.pop(i))
                    continue
            self.deck[j], self.deck[i] = self.deck[i], self.deck[j]

    def deal(self):
        if len(self) <= len(_full_deck_) / 4:
            raise ResourceWarning("low deck")

        return self.deck.pop(0)


if __name__ == "__main__":

    d = DirtyDeck()  # rework as unittests
    print(d)
    print(f"len={len(d)}")

    for rank in [10, "Jack", "Queen", "King", "Ace", "Joker", 2]:
        _ = DirtyDeck(hide=rank)

    try:
        _ = DirtyDeck(hide=15)
    except Exception:
        print("invalid hide fails")
