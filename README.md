# Playing the game of Hex
Hex is a two player board game that is played on a hexagonal grid of any size (typically 11x11). The objective of the game is for players try to build chains of stones from one end of the game board to its opposite end. Gameplay involves players taking turns in placing stones unto the empty cells on the grid. Stones played on the grid cannot be captured or replaced. A hex game ends when one player is able to form an unbroken chain across the board. One interesting thing about hex is that the first player always has a better chance of winning.

This repository contains code for a couple of AI agents that try to play the game of hex. There are two classes of agents: those based on Alpha-Beta search algorithm, and those based on the Monte-Carlo Tree Search algorithm. For the alphabeta implementations, there are two different evaluation functions: max-flow and y-reduction.

## Running the code.
Other than Python 3, this code has no dependencies. After cloning the repository, you can execute on the command line with the following format:

     python main.py [black_player] [white_player]

In this, `[black_player]` and `[white_player]` can be specified as follows:

- `ab-flow:x` for Alpha Beta search with the max flow heuristic, where x is a number that represents the maximum search depth.
- `ab-yred:x` for Alpha Beta search with the y-reduction heuristic, where x is a number that represents the maximum search depth.
- `mcts:x` or  `emcts:x` for Random MCTS and Extended mcts respectively, where x represents the search cutoff time in seconds. 
- `human:` to play as human by entering moves through the keyboard.

For example to play against alpha beta with flow heuristics:

    python main.py human: ab-flow:4

Or mcts vs alpha beta

    python main.py mcts:60 ab-yred:3


