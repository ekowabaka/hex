from hex import representation, players
import time

boardsize = 6

def getmove():
    while True:
        location = input("\nEnter location to place marker (x,y):")
        coords = [int(x) for x in location.split(',')]
        if (coords[0], coords[1]) not in board.markers:
            break
        else:
            print('Invalid move please select another location')
    return coords

if __name__ == "__main__":
    board = representation.Board()
    board.setup(boardsize)
    player = players.AlphaBeta(board) #AlphaBeta(boardsize)

    # board.addmarker(1, 2, representation.WHITE_MARKER)
    # board.addmarker(2, 2, representation.BLACK_MARKER)
    # board.addmarker(2, 1, representation.WHITE_MARKER)
    # board.addmarker(3, 1, representation.BLACK_MARKER)
    # board.addmarker(3, 0, representation.WHITE_MARKER)
    # board.addmarker(0, 2, representation.BLACK_MARKER)
    # board.addmarker(3, 0, representation.WHITE_MARKER)
    # board.addmarker(0, 1, representation.BLACK_MARKER)
    # board.addmarker(0, 3, representation.WHITE_MARKER)
    # print(board.whitegraph.graph)
    # nu = representation.Board()
    # nu.setup(board.size, board.state)
    # print(nu.whitegraph.graph)


    #
    # # board.addmarker(2, 1, representation.WHITE_MARKER)
    # # board.addmarker(3, 1, representation.BLACK_MARKER)
    # # board.addmarker(0, 2, representation.WHITE_MARKER)
    # # board.addmarker(4, 2, representation.BLACK_MARKER)
    # # board.addmarker(3, 2, representation.WHITE_MARKER)
    # board.draw()
    # print(player.evaluate(board))

    print(player.getflow(board.blackgraph))
    print(player.getflow(board.whitegraph))
    # board.addmarker(0, 0, representation.WHITE_MARKER)
    # print(player.getflow(board.blackgraph))
    # print(player.getflow(board.whitegraph))

    while True:
        start = time.time()
        move = getmove() #player.getmove(board)
        print('Elapsed', time.time() - start)
        print(move)
        board.addmarker(move[0], move[1], representation.BLACK_MARKER)
        board.draw()
        print(player.getflow(board.blackgraph), player.getflow(board.whitegraph))
        coords = getmove()
        board.addmarker(coords[0], coords[1], representation.WHITE_MARKER)
        board.draw()
        print(player.getflow(board.blackgraph), player.getflow(board.whitegraph))


