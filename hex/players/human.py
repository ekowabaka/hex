class Default(object):
    """
    A class for the human player.
    """

    def getmove(self, board):
        """
        Retrieve the location where the stone should be placed through the console.
        """
        alphas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        while True:
            location = input(
                "\nEnter location to place marker. \nEg. A1 for the top left cell or H8 for the bottom right cell:").upper()
            coords = (alphas.index(location[0]), int(location[1]) - 1)
            if (coords[0], coords[1]) not in board.markers:
                break
            else:
                print('Invalid move please select another location')
        return tuple(coords)
