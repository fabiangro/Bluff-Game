from typing import Dict, List, Any, Tuple, Union
from random import randint
from game.player import Player
from game.deck import Deck
from game.card import Card
from game.hands import *


class BluffGame:
    """ Representation of the Bluff Game
    """

    min_players = 2
    max_players = 8
    max_cards = 6
    Status = Union[str, Dict[str, Any]]

    def __init__(self) -> None:
        #: The dictionary with ID as a key and corresponding Player object as value.
        self.players: Dict[int: Player] = {}

        #: The list of all players' cards in current turn.
        self.cards_in_use: List[Card] = []

        #: Current turn
        self.turn: int = 0

        #: Boolean value representing if the game has started.
        self.has_started: bool = False

        #: Boolean value representing if the game was won.
        self.win: bool = False

        #: The deck of the cards.
        self.deck: Deck = Deck()

        #: List of done moves in current turn.
        self.moves: List[Tuple[str, List[str]]] = []

        #: Boolean value representing if any player has checked the last move.
        self.checked: bool = False

        #: Player who checked, who was checked, who gets the card, Eliminated?
        self.check_result: List[str, str, str, bool] = ["", "", "", False]

    def is_full(self) -> bool:
        """Check if the game is full.

        :return: True if the game is full, False otherwise.
        """
        return self.active_players_num() >= self.max_players

    def start(self) -> None:
        """Start the game.
        """
        self.has_started = True
        self.deck.shuffle()
        self.deal_cards()

    def reset_turn(self) -> None:
        """Reset the game state in order to start a new turn.
        """
        self.cards_in_use = []
        self.has_started = False
        self.deck = Deck()
        self.moves = []
        self.checked = False
        self.win = False
        self.empty_hands()
        for player in self.players.values():
            player.ready = False

    def reset_game(self) -> None:
        """Reset the game in order to start new game
        """
        self.turn = randint(0, self.all_players_num() - 1)
        for player in self.players.values():
            player.lost = False
            player.cards = 1

        self.reset_turn()

    def deal_cards(self) -> None:
        """Deal cards to the players.
        """
        for player in self.players.values():

            if player.cards != len(player.hand):
                for cards in range(player.cards):
                    card = self.deck.pop_card()
                    self.cards_in_use.append(card)
                    player.give_card(card)

    def add_player(self, player_id: int) -> None:
        """Add a player to the game.

        :param player_id: The unique ID of the player.
        """

        player = Player(player_id)
        self.players[player_id] = player

    def remove_player(self, player_id: int) -> None:
        """Remove a player from the game.

        :param player_id: The unique ID of the player.
        """

        del self.players[player_id]

    def empty_hands(self) -> None:
        """Empty the hands of all players.
        """

        for player in self.players.values():
            player.reset_hand()

    def ready_players(self) -> int:
        """Get the number of ready players.

        :return: Number of ready players
        """

        ready = 0

        for player in self.players.values():
            if not player.lost and player.ready:
                ready += 1

        return ready

    def players_are_ready(self) -> bool:
        """Check if all the active players are ready.

        :return: True if all players are ready, False otherwise.
        """
        return self.ready_players() == self.active_players_num() and self.ready_players() >= self.min_players

    def player_make_action(self, player_id: int, action: str) -> Status:
        """Handle the move/action from the player in the game.

        :param player_id: The unique ID of the player.
        :param action: The action/move by the player.
        :return: Current game state after player action/move
        """

        player_index: int = self.player_index_by_id(player_id)
        current_player: Player = self.players[player_id]

        if self.win:
            if action == "Start":
                self.reset_game()

            return self.get_game_status(current_player)

        elif isinstance(action, str) and action.startswith("name"):
            name = action.split()[1]
            duplicated_name = len(
                [player.name for player in self.players.values()])

            if duplicated_name > 0:
                name += str(duplicated_name)
            current_player.name = action.split()[1]

        elif not self.has_started:
            if self.players_are_ready():
                self.reset_game()
                self.start()

            else:
                if action == "Start":
                    current_player.ready = True

                elif action == "Wait":
                    current_player.ready = False

            return self.get_game_status(current_player)

        elif current_player.lost:
            pass

        elif self.checked:
            if self.players_are_ready():
                if not self.win:
                    self.reset_turn()
                    self.start()

            elif action == "Start":
                current_player.ready = True

            elif action == "Wait":
                current_player.ready = False

            return self.get_game_status(current_player)

        elif action == "check":
            if len(self.moves) < 1:
                pass
            else:
                self.handle_check(current_player)
                return self.get_game_status(current_player)

        elif player_index is not self.turn:
            pass

        elif action == "Get":
            pass

        try:
            if action.startswith("move "):
                action = action.split()
                move = action[1:]

                if self.can_be_played(move):
                    self.moves.append((current_player.name, move))
                    self.next_turn()
        except:
            pass

        else:
            pass

        return self.get_game_status(current_player)

    def can_be_played(self, move: List[str]) -> bool:
        """Check if the move has higher hierarchy than last move in the game.

        :param move: move[0] represents the Hand, the rest are cards values/colors
        :return: True if move can be played, False otherwise.
        """

        if not self.moves:
            return True

        last_move = self.moves[-1][1]
        last_move = self.parse_move(last_move)

        current_move = self.parse_move(move)

        return last_move < current_move

    def handle_check(self, checking_player: Player) -> None:
        """Handle check action in the game.

        :param checking_player: The player who decided to check.
        """

        i = 1

        while True:
            player_being_checked = self.players[self.player_index_to_id(
                (self.turn - i) % self.all_players_num())]

            if not player_being_checked.lost:
                player_being_checked = self.players[self.player_index_to_id(
                    (self.turn - i) % self.all_players_num())]
                break
            else:
                i += 1

        last_move = self.moves[-1][1]
        move = self.parse_move(last_move)

        if self.check(move):
            who_gets_card = checking_player
        else:
            who_gets_card = player_being_checked

        who_gets_card.cards += 1
        eliminated = who_gets_card.cards >= self.max_cards
        self.check_result = [checking_player.name, player_being_checked.name,
                             who_gets_card.name, eliminated]

        self.turn = self.player_index_by_player(who_gets_card)
        self.checked = True

        if eliminated:
            who_gets_card.lost = True
            who_gets_card.cards = 0
            self.next_turn()

        self.player_index_by_player(who_gets_card)

    def get_game_status(self, current_player: Player) -> Status:
        """Get current state of the game

        :param current_player: The player who will receive the game state.
        :return: The current state of the game.
        """

        game_status = {}
        game_status["start"] = self.has_started
        game_status["lost"] = current_player.lost
        game_status["hand"] = current_player.hand
        game_status["win"] = self.win
        game_status["moves"] = self.moves
        game_status["check_result"] = self.check_result
        game_status["checked"] = self.cards_in_use if self.checked else []
        game_status[
            "ready"] = f"Waiting for players {self.ready_players()}/{self.active_players_num()}"
        game_status["players"] = [
            (p.name, p.cards) if p is not current_player and not p.lost
            else ("You: " + p.name, p.cards) for p in self.players.values() if
            not p.lost]
        game_status["is_turn"] = (
                    self.turn == self.player_index_by_player(current_player)) \
            if not current_player.lost else False
        game_status["turn"] = [player.name for player in self.players.values()
                               if self.player_index_by_player(
                player) == self.turn][0]

        return game_status

    def player_index_by_player(self, player: Player) -> int:
        """Get player's index by Player object.

        :param player: The player object.
        :return: The index of the player in list of players.
        """

        for index, name in enumerate(self.players.values()):
            if name is player:
                return index

    def player_index_by_id(self, player_id: int) -> int:
        """Get the player's index by the player's unique ID.

        :param player_id: The unique ID of the player.
        :return: The index of the player in list of players.
        """

        for index, id in enumerate(self.players.keys()):
            if id == player_id:
                return index

    def player_index_to_id(self, index: int) -> int:
        """Get the player's unique ID by the index.

        :param index: The index of the player in list of players.
        :return: The unique ID of the player.
        """

        for cur_index, player in enumerate(self.players.keys()):
            if cur_index == index:
                return player

    def next_turn(self) -> None:
        """Increment the current turn and update game state.
        """
        active_players = [player.name for player in self.players.values() if
                          not player.lost]
        if len(active_players) == 1:
            self.win = active_players[0]

            return

        while True:
            self.turn = (self.turn + 1) % self.all_players_num()
            current_player = self.player_index_to_id(self.turn)

            if not self.players[current_player].lost:
                break

    def all_players_num(self) -> int:
        """Get the number of all players in the game.

        :return: Number of all players in the game.
        """
        return len(self.players)

    def active_players_num(self) -> int:
        """Get the number of active players in the game.

        :return: The number of active players in the game.
        """
        return len(
            [player.id for player in self.players.values() if not player.lost])

    def check(self, mv: Hand) -> bool:
        """Check if the move is in the list of all players cards.

        :param mv: Representation of the move.
        :return: True if move is present in all player cards, False otherwise.
        """

        mv_rank = mv.hierarchy_rank()
        cards = self.cards_in_use

        if mv_rank == 0:  # HighCard
            res = Card.high_card(cards, Card(mv.value))

        elif mv_rank == 1:  # Pair
            res = Card.pair(cards, Card(mv.value))

        elif mv_rank == 2:  # TwoPairs
            res = Card.two_pair(cards, Card(mv.value1), Card(mv.value2))

        elif mv_rank == 3:  # Straight
            if mv.small:  # Small Straight
                res = Card.small_straight(cards)
            else:  # Big Straight
                res = Card.big_straight(cards)

        elif mv_rank == 4:  # ThreeOfKind
            res = Card.three(cards, Card(mv.value))

        elif mv_rank == 5:  # Flush
            res = Card.flush(cards, mv.color)

        elif mv_rank == 6:  # FullHouse
            res = Card.full(cards, mv.value_of_three, mv.value_of_two)

        elif mv_rank == 7:  # FourOfKind
            res = Card.four(cards, Card(mv.value))

        elif mv_rank == 8:  # Poker
            if mv.small:  # Small
                res = Card.small_poker(cards, mv.color)
            else:
                res = Card.big_poker(cards, mv.color)
        else:
            raise Exception("Invalid move")

        return res

    @staticmethod
    def parse_move(move: List[str]) -> Hand:
        """Parse move to Hand object.

        :param move: move[0] represents the Hand, the rest are cards values/colors
        :return: Hand object representation of the move.
        """

        hand = move[0]

        if hand == "HighCard":
            return HighCard(move[1])

        elif hand == "Pair":
            return Pair(move[1])

        elif hand == "TwoPairs":
            return TwoPairs(move[1], move[2])

        elif hand == "SmallStraight":
            return Straight()

        elif hand == "BigStraight":
            return Straight(False)

        elif hand == "ThreeOfKind":
            return ThreeOfKind(move[1])

        elif hand == "Flush":
            return Flush(move[1])

        elif hand == "FullHouse":
            return FullHouse(move[1], move[2])

        elif hand == "FourOfKind":
            return FourOfKind(move[1])

        elif hand == "SmallPoker":
            return Poker(move[1])

        elif hand == "BigPoker":
            return Poker(move[1], False)

        else:
            print("invalid input")
