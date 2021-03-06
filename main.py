from hex import representation
from hex.players import alphabeta, human, mcts
import sys

boardsize = 8
players = [None, None]
wins = [0, 0]
session = [""]
movelist = []


def isdone(board):
    """
    Checks if any of the players have completed the chain, so the game could end.
    """
    if board.isend():
        print("White" if board.winner == representation.WHITE_MARKER else "Black", "wins!")
        file = open(session[0] + "p1", 'w')
        for line in players[0].stats:
            for value in line.values():
                file.write(str(value) + ",")
            file.write("\n")
        file.close()

        file = open(session[0] + "p2", 'w')
        for line in players[1].stats:
            for value in line.values():
                file.write(str(value) + ",")
            file.write("\n")
        file.close()

        open(session[0] + "moves", "w").write(str(movelist))

        return True
    return False


def playerfactory(desc, board, marker):
    """
    Parse the command line argument and create objects for the players.
    Command line arguments are in the format [type]:[options].
    """
    desc = desc.split(':')
    session[0] += desc[0] + "-" + desc[1] + "-"
    player = None
    if desc[0] == "human":
        player = human.Default()
    elif desc[0] == "ab-flow":
        player = alphabeta.FlowAlphaBeta(board, marker)
        player.maxdepth = int(desc[1])
    elif desc[0] == "ab-yred":
        player = alphabeta.YReductionAlphaBeta(board, marker)
        player.maxdepth = int(desc[1])
    elif desc[0] == "mcts":
        player = mcts.PureRandomUCT(marker)
        player.maxtime = int(desc[1])
        if 2 in desc:
            player.selection = desc[2]
    elif desc[0] == "emcts":
        player = mcts.ExtendedMCTS(marker)
        player.maxtime = int(desc[1])
        if 2 in desc:
            player.selection = desc[2]
    else:
        print("Unknown player type", desc)
        quit()
    return player


def run(p1, p2):
    """
    Run a match between two players: p1 and p2.
    """
    board = representation.Board()
    board.setup(boardsize)
    players[0] = playerfactory(p1, board, representation.BLACK_MARKER)
    players[1] = playerfactory(p2, board, representation.WHITE_MARKER)

    while True:
        board.draw()
        if isdone(board):
            break
        move = players[0].getmove(board)
        print("Played", board.printmove(move))
        print()
        movelist.append(move)
        board.addmarker(move[0], move[1], representation.BLACK_MARKER)
        board.draw()
        if isdone(board):
            break
        move = players[1].getmove(board)
        print("Played", board.printmove(move))
        print()
        movelist.append(move)
        board.addmarker(move[0], move[1], representation.WHITE_MARKER)
    return board.winner


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
