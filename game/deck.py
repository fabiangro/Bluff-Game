from random import shuffle
from typing import List
from game.card import Card


class Deck:
    """Represents a deck of playing cards.
    """

    def __init__(self) -> None:
        #: Represents full 54 cards deck, including 2 joker cards.
        self.deck = self.create_deck()

    def create_deck(self) -> List[Card]:
        """Creates a new deck of cards.

        :return: The list of cards in the deck.
        """
        deck = [Card(0, 0), Card(0, 0)]

        for value in range(2, 15):
            for color in range(1, 5):
                deck.append(Card(value, color))

        return deck

    def pop_card(self) -> Card:
        """Removes and returns the top card from the deck.

        :return: The top card from the deck.
        """
        return self.deck.pop()

    def shuffle(self) -> None:
        """Shuffles the deck."""
        shuffle(self.deck)
