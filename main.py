from hex import representation
from hex.players import alphabeta, human, mcts

boardsize = 8

def isdone(board):
    if board.isend():
        print("White" if board.winner == representation.WHITE_MARKER else "Black", "wins!")
        quit()

if __name__ == "__main__":
    board = representation.Board()
    board.setup(boardsize)
    player1 = alphabeta.FlowAlphaBeta(board, representation.BLACK_MARKER)
    player2 = mcts.PureRandomUCT(representation.WHITE_MARKER)

    # positions = {(0, 1): 0, (1, 2): 0, (3, 2): 0, (1, 3): 0, (3, 3): 1, (3, 0): 1, (3, 1): 1, (2, 1): 0, (0, 2): 0, (2, 0): 0, (0, 0): 1, (2, 3): 0, (2, 2): 1, (1, 0): 1, (0, 3): 1, (1, 1): 0}
    #
    # board.usegraphs = False
    #
    # for pos, marker in positions.items():
    #     board.addmarker(pos[0], pos[1], marker)
    #
    # board.draw()
    # print(board.isend() is False)
    # quit()

    while True:
        board.draw()
        isdone(board)
        move = player1.getmove(board)
        print(move)
        board.addmarker(move[0], move[1], representation.BLACK_MARKER)
        board.draw()
        isdone(board)
        move = player2.getmove(board)
        board.addmarker(move[0], move[1], representation.WHITE_MARKER)
        print(move)
