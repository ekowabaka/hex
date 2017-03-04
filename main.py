from hex import representation
from hex.players import alphabeta, human, mcts

boardsize = 8

def isdone(board):
    winner = board.getwin()
    if winner is not None:
        print("White" if winner == representation.WHITE_MARKER else "Black", "wins!")
        quit()

if __name__ == "__main__":
    board = representation.Board()
    board.setup(boardsize)
    player1 = mcts.PureRandomUCT(representation.BLACK_MARKER)
    player2 = alphabeta.FlowAlphaBeta(board, representation.WHITE_MARKER)

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
