from hex import representation, players

boardsize = 5

if __name__ == "__main__":
    board = representation.Board()
    board.setup(boardsize)
    network = players.AlphaBeta(boardsize)

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
    #
    # # board.addmarker(2, 1, representation.WHITE_MARKER)
    # # board.addmarker(3, 1, representation.BLACK_MARKER)
    # # board.addmarker(0, 2, representation.WHITE_MARKER)
    # # board.addmarker(4, 2, representation.BLACK_MARKER)
    # # board.addmarker(3, 2, representation.WHITE_MARKER)
    # board.draw()
    # print(network.evaluate(board))

    # print(network.getflow(board.blackgraph))
    # print(network.getflow(board.whitegraph))
    # board.addmarker(0, 0, representation.WHITE_MARKER)
    # print(network.getflow(board.blackgraph))
    # print(network.getflow(board.whitegraph))

    while True:
        move = network.getmove(board)
        print(move)
        board.addmarker(move[0], move[1], representation.BLACK_MARKER)
        board.draw()
        location = input("\nEnter location to place marker (x,y):")
        coords = [int(x) for x in location.split(',')]
        board.addmarker(coords[0], coords[1], representation.WHITE_MARKER)
        board.draw()

