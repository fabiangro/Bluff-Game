from typing import List, Union


class Card:
    """Represents a playing card.

    :param value: The value of the card.
    :param color: The color of the card.
    """

    CardType = Union['Card', str, int]
    colors = {1: "clubs", 2: "diamonds", 3: "hearts", 4: "spades"}
    color_to_num = {"club": 1, "diamond": 2, "hearts": 3, "spades": 4}
    values = {**{i: i for i in range(2, 11)}, **{0: "joker", 11: "jack", 12: "queen", 13: "king", 14: "ace"}}

    def __init__(self, value: int, color: int = 1) -> None:
        # The value of the card
        #: 0 (Joker), 2, 3, ... , 10, 11 (Jack), 12 (Queen), 13 (King), 14 (Ace)
        self.value = value

        # The color of the card.
        # 1 (Clubs), 2 (Diamonds), 3 (Hearts), 4 (Spades)
        self.color = color

    def __hash__(self) -> int:
        return hash(self.value)

    def __lt__(self, other: CardType) -> bool:
        """Checks if this card is less than another card.

        :param other: The other card to compare.
        :return: True if this card is less than the other card, False otherwise.
        """

        if self.value == 0:
            return True
        elif type(other) == int:
            return self.value < other
        elif type(other) == str:
            return self.color < self.color_to_num[other]
        elif other.value == 0:
            return True
        return self.value < other.value

    def __eq__(self, other: CardType) -> bool:
        """Checks if this card is equal to another card.

        :param other: other (CardType): The other card to compare.
        :return: True if this card is equal to the other card, False otherwise.
        """

        if self.value == 0:
            return True
        elif type(other) == int:
            return self.value == other
        elif type(other) == str:
            return self.colors[self.color] == other.lower()
        elif other.value == 0:
            return True

        return self.value == other.value

    def __str__(self) -> str:
        """Returns a string representation of the card.

        :return: The string representation of the card.
        """

        if self.value == 0:
            return "joker"
        else:
            value = self.values[self.value]
            color = self.colors[self.color]
            return f"{value}_of_{color}"

    def __repr__(self) -> str:
        """Returns a string representation of the card.

        :return: The string representation of the card.
        """

        if self.value == 0:
            return "joker"
        return f"({self.colors[self.color]} {self.values[self.value]})"

    def __add__(self, other: CardType) -> CardType:
        """Adds two cards or a card and a value.

        :param other: The other card or value to add.
        :return: CardType: The result of the addition.
        """

        if self.value == 0:
            return Card(0, 0)
        elif type(other) == int:
            return Card(self.value + other, self.color)
        return Card(self.value + other.value, self.color)

    def __iadd__(self, other: CardType) -> CardType:
        """Adds a card or a value to this card.

        :param other: The other card or value to add.
        :return: The updated card.
        """

        if self.value == 0:
            pass
        else:
            if type(other) == int:
                self.value += other
            else:
                self.value += other.value
            return self

    @staticmethod
    def high_card(cards: List[CardType], card: CardType) -> bool:
        """Checks if a given card is present in a list of cards.

        :param cards: The list of cards to check.
        :param card: _The card to look for.
        :return: True if the card is present, False otherwise.
        """

        return card in cards

    @staticmethod
    def pair(cards: List[CardType], card: CardType):
        """Checks if there is a pair of a given card in a list of cards.

        :param cards: The list of cards to check.
        :param card: The card to look for.
        :return: True if a pair is present, False otherwise.
        """

        return cards.count(card) >= 2

    @staticmethod
    def two_pair(cards: List[CardType], card1: CardType, card2: CardType) -> bool:
        """Checks if there are two pairs of two given cards in a list of cards.

        :param cards: The list of cards to check.
        :param card1: The first card to look for.
        :param card2: The second card to look for.
        :return: True if two pairs are present, False otherwise.
        """

        return Card.pair(cards, card1) and Card.pair(cards, card2)

    @staticmethod
    def three(cards: List[CardType], card: CardType) -> bool:
        """Checks if there are three of a given card in a list of cards.

        :param cards: The list of cards to check.
        :param card: The card to look for.
        :return: True if three cards are present, False otherwise.
        """

        return cards.count(card) >= 3

    @staticmethod
    def small_straight(cards: List[CardType]) -> bool:
        """Checks if there is a small straight in a list of cards.

        :param cards: The list of cards to check.
        :return: True if a small straight is present, False otherwise.
        """

        joker_count = cards.count(0)
        order = joker_count

        for i in range(joker_count):
            cards.remove(0)

        cards = sorted(list(set(cards)))

        for i in range(len(cards) - 4):
            if cards[i].value >= 10:
                break
            else:
                if cards[i] + 1 == cards[i + 1]:
                    order += 1
                if cards[i + 1] + 1 == cards[i + 2]:
                    order += 1
                if cards[i + 2] + 1 == cards[i + 3]:
                    order += 1
                if cards[i + 3] + 1 == cards[i + 4]:
                    order += 1

                if order >= 4:
                    return True
                else:
                    order = joker_count

        return False

    @staticmethod
    def big_straight(cards: List[CardType]) -> bool:
        """Checks if there is a big straight in a list of cards.

        :param cards: The list of cards to check.
        :return: True if a big straight is present, False otherwise.
        """

        joker_count = cards.count(0)
        for i in range(joker_count):
            cards.remove(0)

        straight_counter = joker_count

        for value in range(10, 15):
            if value in cards:
                straight_counter += 1

        return straight_counter >= 5


    @staticmethod
    def flush(cards: List[CardType], color: str) -> bool:
        """Checks if there is a flush of a given color in a list of cards.

        :param cards: The list of cards to check.
        :param color: The color to look for.
        :return: True if a flush is present, False otherwise.
        """

        return cards.count(color) >= 5

    @staticmethod
    def full(cards: List[CardType], card3: CardType, card2: CardType) -> bool:
        """Checks if there is a full house with a given three of a kind and a pair in a list of cards.

        :param cards: The list of cards to check.
        :param card3: The three of a kind card.
        :param card2: _The pair card.
        :return: True if a full house is present, False otherwise.
        """

        return Card.three(cards, card3) and Card.pair(cards, card2)

    @staticmethod
    def four(cards: List[CardType], card: CardType) -> bool:
        """Checks if there are four of a given card in a list of cards.

        :param cards: The list of cards to check.
        :param card: The card to look for.
        :return: True if four cards are present, False otherwise.
        """

        return cards.count(card) >= 4

    @staticmethod
    def small_poker(cards: List[CardType], color: str) -> bool:
        """Checks if there is a small poker of a given color in a list of cards.

        :param cards: The list of cards to check.
        :param color: The color to look for.
        :return: True if a small poker is present, False otherwise.
        """

        cards = [card for card in cards if card == color]

        joker_count = cards.count(0)
        for i in range(joker_count):
            cards.remove(0)

        cards = sorted(list(set(cards)))
        print(cards)
        order = joker_count

        for i in range(len(cards) - 4):
            if cards[i].value >= 10:
                break
            else:
                if cards[i] + 1 == cards[i + 1]:
                    order += 1
                if cards[i + 1] + 1 == cards[i + 2]:
                    order += 1
                if cards[i + 2] + 1 == cards[i + 3]:
                    order += 1
                if cards[i + 3] + 1 == cards[i + 4]:
                    order += 1

                if order >= 4:
                    return True
                else:
                    order = joker_count
        return False

    @staticmethod
    def big_poker(cards: List[CardType], color: str) -> bool:
        """Checks if there is a big poker of a given color in a list of cards.

        :param cards: The list of cards to check.
        :param color: The color to look for.
        :return: True if a big poker is present, False otherwise.
        """

        cards = sorted(cards)
        joker_count = cards.count(0)

        for i in range(joker_count):
            cards.remove(0)

        poker_list = []
        for card in cards:
            if card in range(10, 15) and card == color:
                poker_list.append(card)

        for i in range(joker_count):
            poker_list.append(0)

        if len(poker_list) >= 5:
            return True

        return False
