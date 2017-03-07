This software requires Python 3.5+. It has only been tested on Linux.

Execute with the following format

     python3 main.py [black_player] [white_player]

[black_player] and [white_player] can be specified as follows:

    ab-flow:x and ab-yred:x for Alpha Beta with max flow and y reduction heuristics respectively. x is a number that
    represents maximum search depth.

    mcts:x emcts:x for Random MCTS and Extended mcts respectively. x is a number that represents cut off time in
    seconds.

    human: to play as human

For example to play against alpha beta with flow heuristics:

    python3 main.py human: ab-flow:4

Or mcts vs alpha beta

    python3 main.py mcts:60 ab-yred:3

Thanks!

