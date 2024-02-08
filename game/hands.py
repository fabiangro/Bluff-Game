class Hand:
    """Representation of the poker hand."""

    value, value1, value2, color, value_of_two, value_of_three, small = 0, 0, 0, 0, 0, 0, 0

    @staticmethod
    def parse(value: str) -> str:
        """Parse the value of a card.

        :param value: The value of the card.
        :return: The parsed value of the card.
        """
        cards = {
            **{"joker": 0, "jack": 11, "queen": 12, "king": 13, "ace": 14},
            **{str(i): i for i in range(2, 11)}}

        if value in ["Clubs", "Diamonds", "Hearts", "Spades"]:
            return value
        else:
            return cards[value.lower()]

    def hierarchy_rank(self) -> None:
        """Determine the hierarchy rank of the hand."""
        pass

    def __lt__(self, other: 'Hand') -> bool:
        """Compare two hands based on their hierarchy rank.

        :param other:The other hand to compare.
        :return: True if the current hand is less than the other hand, False otherwise.
        """
        colors = {"Clubs": 1, "Diamonds": 2, "Hearts": 3, "Spades": 4}

        if isinstance(other, Hand):
            hierarchy1 = self.hierarchy_rank()
            hierarchy2 = other.hierarchy_rank()

            if hierarchy1 == hierarchy2:
                if hierarchy1 == 0:  # HighCard
                    return self.value < other.value

                elif hierarchy1 == 1:  # Pair
                    return self.value < other.value

                elif hierarchy1 == 2:  # TwoPairs
                    self_value1 = self.value1
                    self_value2 = self.value2
                    other_value1 = other.value1
                    other_value2 = other.value2
                    # 1/2  2/3
                    bool1 = self_value1 < other_value1 and self_value1 < other_value2
                    bool2 = self_value2 < other_value1 and self_value2 < other_value2

                    return bool1 or bool2

                elif hierarchy1 == 3:  # Straight
                    if self.small and other.small:
                        return False
                    elif not self.small and not other.small:
                        return False
                    else:
                        return self.small and not other.small

                elif hierarchy1 == 4:  # ThreeOfKind
                    return self.value < other.value

                elif hierarchy1 == 5:  # Flush
                    return colors[self.color] < colors[other.color]

                elif hierarchy1 == 6:  # FullHouse
                    if self.value_of_three == other.value_of_three:
                        return self.value_of_two < other.value_of_two
                    else:
                        return self.value_of_three < other.value_of_three

                elif hierarchy1 == 7:  # FourOfKind
                    return self.value < other.value

                elif hierarchy1 == 8:  # Poker
                    if self.small and other.small:
                        return colors[self.color] < colors[other.color]
                    elif not self.small and not other.small:
                        return colors[self.color] < colors[other.color]
                    else:
                        return self.small and not other.small
            else:
                return hierarchy1 < hierarchy2


class HighCard(Hand):
    """Representation of a high card hand.

    :param value: The value of the card.
    """

    def __init__(self, value: str) -> None:
        self.value = self.parse(value)

    def hierarchy_rank(self) -> int:
        """Get the hierarchy rank of the high card hand.

        :return: The hierarchy rank.
        """
        return 0


class Pair(Hand):
    """Representation of a pair's hand.

    :param value: The value of the card.
    """

    def __init__(self, value: str) -> None:
        self.value = self.parse(value)

    def hierarchy_rank(self) -> int:
        """Get the hierarchy rank of the high card hand.

        :return: The hierarchy rank.
        """
        return 1


class TwoPairs(Hand):
    """Representation of a two pairs hand.

    :param value1: The value of the first pair.
    :param value2: The value of the second pair.
    """

    def __init__(self, value1: str, value2: str) -> None:
        self.value1 = self.parse(value1)
        self.value2 = self.parse(value2)

    def hierarchy_rank(self) -> int:
        """Get the hierarchy rank of the high card hand.

        :return: The hierarchy rank.
        """
        return 2


class Straight(Hand):
    """Representation of a straight hand.

    :param small: True if the straight is small, False if it's big.
    """

    def __init__(self, small: bool = True) -> None:
        self.small = small

    def hierarchy_rank(self) -> int:
        """Get the hierarchy rank of the high card hand.

        :return: The hierarchy rank.
        """
        return 3


class ThreeOfKind(Hand):
    """Representation of a three of a kind hand.

    :param value: The value of the card.
    """

    def __init__(self, value: str) -> None:
        self.value = self.parse(value)

    def hierarchy_rank(self) -> int:
        """Get the hierarchy rank of the high card hand.

        :return: The hierarchy rank.
        """
        return 4


class Flush(Hand):
    """Representation of a flush hand.

    :param color: The color of the flush.
    """

    def __init__(self, color: str) -> None:
        self.color = color

    def hierarchy_rank(self) -> int:
        """Get the hierarchy rank of the high card hand.

        :return: The hierarchy rank.
        """
        return 5


class FullHouse(Hand):
    """Representation of a full house hand.

    :param value_of_three: The value of the three of a kind.
    :param value_of_two: The value of the pair.
    """

    def __init__(self, value_of_three: str, value_of_two: str) -> None:
        self.value_of_three = self.parse(value_of_three)
        self.value_of_two = self.parse(value_of_two)

    def hierarchy_rank(self) -> int:
        """Get the hierarchy rank of the high card hand.

        :return: The hierarchy rank.
        """
        return 6


class FourOfKind(Hand):
    """Representation of a four of a kind hand.

    :param value: The value of the card.
    """

    def __init__(self, value: str) -> None:
        self.value = self.parse(value)

    def hierarchy_rank(self) -> int:
        """Get the hierarchy rank of the high card hand.

        :return: The hierarchy rank.
        """
        return 7


class Poker(Hand):
    """Representation of a poker hand.

    :param color: The color of the poker.
    :param small: True if the poker is small, False if it's big.
    """

    def __init__(self, color: str, small: bool = True) -> None:
        self.color = color
        self.small = small

    def hierarchy_rank(self) -> int:
        """Get the hierarchy rank of the high card hand.

        :return: The hierarchy rank.
        """
        return 8
