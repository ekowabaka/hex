
class Default(object):
    def getmove(self, board):
        while True:
            location = input("\nEnter location to place marker (x,y):")
            coords = [int(x) for x in location.split(',')]
            if (coords[0], coords[1]) not in board.markers:
                break
            else:
                print('Invalid move please select another location')
        return tuple(coords)