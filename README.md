# Bluff Game

This is my python project for Object-Oriented Programming course at the University of Wroclaw (summer semester 2022/2023).

## Description
This project is an implementation of a card game that can be played online with multiple players. It utilizes the Pygame library for the graphical interface and socket programming for networking functionality. Players can connect to a server and play the card game together over the network.

## Features
- Multiplayer online card game
- Graphical interface built with Pygame
- Socket programming for networking
- Support for multiple players connecting to a server
- Interactive gameplay experience

## About game

Bluff Game is a card game that utilizes a standard 52-card deck with two additional jokers. The jokers can be considered as any card. The game accommodates 2-10 players, although the recommended number for optimal gameplay is between 5-8 players.
The game is based on guessing and anticipating possible Poker Hand Rankings, but their hierarchy is a bit modified.

## Gameplay

1. At the beginning of each game, each player is dealt one card. Then, a chosen player starts the round.

2. Each player, when it is their turn, makes move by indicating a hand ranking they believe is present in the pool of all players' cards. The hand must be higher in hierarchy than the one indicated by the previous player.

3. At any point during the active round, any player can "check" the last indicated hand ranking. Then, all players reveal their cards, and it is verified whether the last indicated hand ranking is indeed present in the pool of cards.

4. A new round begins, with one player receiving an additional card. The player who called the last hand ranking receives  the additional card if the indicated hand was present. Otherwise the player who indicated that hand receives the card.

5. The next round begins with the player who received the additional card.

6. A player who got 6th card is eliminated from the game.

7. The game ends when only one player remains, who is declared the winner.

Hand rankings hierarchy from the lowest to the highest:
1. High card (One card value),
Pair (2 cards with the same value),
2. Two pairs,
3. Small straight (5 cards in row, without Jack-Ace),
4. Big straight (5 cards in row from Jack to Ace)
5. Three of kind (3 cards with the same value),
6. Flush (5 cards with the same color),
7. Full House (Pair and Three of kind),
8. Four of kind (4 cards with the same value),
8. Small Poker (small straight, but with all cards in the same color),
9. Big Poker (big straight, but with all cards in the same color)

Colors ranking from the lowest to the highest:
clubs, diamonds, hearts, spades

One hand ranking is considered higher than the same hand ranking, if it includes card with higher value, or color with higher value.

## Screenshot from the game:
![Screenshot from 2024-02-08 01-10-37](https://github.com/fabiangro/Bluff-Game/assets/118316299/b7ddb084-53e4-4e75-9eae-845d6207f30a)

## Installing requirements

```bash
pip install -r requirements.txt
```

## How to run
By the default the server is created locally on the port 5556, you can modify it by changing SERVER_IP, SERVER_PORT variables in run_server.py and run_client.py files.

To run the server:
```bash
python run_server.py
```
To run the client:
```bash
python run_client.py
```
