
class Default(object):
    def getmove(self, board):
        alphas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        board.draw()
        while True:
            location = input("\nEnter location to place marker. \nEg. A1 for the top left cell or H8 for the bottom right cell:").upper()
            coords = (alphas.index(location[0]), int(location[1]) - 1)
            if (coords[0], coords[1]) not in board.markers:
                break
            else:
                print('Invalid move please select another location')
        return tuple(coords)