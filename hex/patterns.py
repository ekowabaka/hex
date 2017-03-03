class Search(object):
    def __init__(self):
        self.bridges = list()
        self.bridges.append({"size": (2, 2), "pattern": (1, None, None, 1), "offset": 0})
        self.bridges.append({"size": (2, 3), "pattern": (1, None, None, 1), "offset": 1})
        self.bridges.append({"size": (3, 2), "pattern": (None, 1, 1, None), "offset": 1})

        self.prunepattern = ((1,-2), (-1,-1), (0,-1), (1,-1), (2,-1), (-1,0), (0,0), (1,0), (-2,1), (-1,1), (0,1), (1,1), (-1,2))

    def extract(self, state, bridge, offset, marker):
        substate = list()
        for y in range(bridge['size'][1]):
            for x in range(bridge['size'][0]):
                statemarker = state[x + offset[0]][y + offset[1]]
                if statemarker == marker:
                    substate.append(1)
                elif statemarker == None:
                    substate.append(None)
                else:
                    substate.append(0)
        return tuple(substate[bridge['offset']:len(bridge['pattern']) + 1])

    def countbridges(self, board, marker):
        """
        Find bridges to be used as a feature for search
        :param board:
        :param marker:
        :return:
        """
        numbridges = 0
        for bridge in self.bridges:
            for x in range(board.size - bridge['size'][0]):
                for y in range(board.size - bridge['size'][1]):
                    if self.extract(board.state, bridge, (x, y), marker) == bridge['pattern']:
                        numbridges+=1
        return numbridges

    def getpattern(self, board):
        moves = set()
        for pos, marker in board.markers.items():
            for x, y in self.prunepattern:
                if pos[0] + x >= 0 and pos[1] + y >= 0:
                    moves.add((pos[0] + x, pos[1] + y))
        if not moves:
            for x in range(2, board.size - 2):
                for y in range(2, board.size - 2):
                    moves.add((x, y))
        return moves

