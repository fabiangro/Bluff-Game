from typing import List
from game.card import Card


class Player:
    """Represents a player in a card game.

    :param id: The player's ID.
    """

    def __init__(self, id: int) -> None:
        #: The player's ID.
        self.id: int = id

        #: The player's name.
        self.name: str = ""

        #: Number of cards in player's hand.
        self.cards: int = 1

        #: List of cards in player's hand.
        self.hand: List[Card] = []

        #: Bool value representing if the player lost the game.
        self.lost: bool = False

        #: Bool value representing if the player is ready.
        self.ready: bool = False

    def give_card(self, card: Card) -> None:
        """Adds a card to the player's hand.

        :param card: The card to be added.
        """
        self.hand.append(card)

    def add_card(self) -> None:
        """Increases the number of cards held by the player by 1."""
        self.cards += 1

    def reset_hand(self) -> None:
        """Resets the player's hand by removing all cards."""
        self.hand = []
