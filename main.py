from hex import representation
from hex.players import alphabeta, human, mcts
import sys

boardsize = 8
player1 = None
player2 = None
session = [""]
movelist = []

def isdone(board):
    if board.isend():
        print("White" if board.winner == representation.WHITE_MARKER else "Black", "wins!")
        file = open(session[0] + "p1", 'w')
        for line in player1.stats:
            for value in line.values():
                file.write(str(value) + ",")
            file.write("\n")
        file.close()

        file = open(session[0] + "p2", 'w')
        for line in player2.stats:
            for value in line.values():
                file.write(str(value) + ",")
            file.write("\n")
        file.close()

        open(session[0] + "moves", "w").write(str(movelist))

        return True
    return False

def playerfactory(desc, board, marker):
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
    elif desc[0] == "emcts":
        player = mcts.ExtendedMCTS(marker)
        player.maxtime = int(desc[1])
    else:
        print("Unknown player type", desc)
        quit()
    return player

if __name__ == "__main__":
    board = representation.Board()
    board.setup(boardsize)

    if sys.argv[1]:
        player1 = playerfactory(sys.argv[1], board, representation.BLACK_MARKER)
    if sys.argv[2]:
        player2 = playerfactory(sys.argv[2], board, representation.WHITE_MARKER)

    while True:
        board.draw()
        if isdone(board): break
        move = player1.getmove(board)
        movelist.append(move)
        board.addmarker(move[0], move[1], representation.BLACK_MARKER)
        board.draw()
        if isdone(board): break
        move = player2.getmove(board)
        movelist.append(move)
        board.addmarker(move[0], move[1], representation.WHITE_MARKER)
