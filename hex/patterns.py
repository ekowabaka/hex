class Search(object):
    def __init__(self):
        self.bridges = list()
        self.bridges.append({"size": (2, 2), "pattern": (1, 0, None, 1), "interest": (0, 1)})
        self.bridges.append({"size": (2, 2), "pattern": (1, None, 0, 1), "interest": (1, 0)})
        self.bridges.append({"size": (2, 3), "pattern": (2, 1, 0, None, 1, 2), "interest": (1, 1)})
        self.bridges.append({"size": (2, 3), "pattern": (2, 1, None, 0, 1, 2), "interest": (0, 1)})
        self.bridges.append({"size": (3, 2), "pattern": (2, None, 1, 1, 0, 2), "interest": (1, 0)})
        self.bridges.append({"size": (3, 2), "pattern": (2, 0, 1, 1, None, 2), "interest": (1, 1)})

        self.dead = list()
        self.dead.append({"size": (3, 2), "pattern": (2, 1, 1, 1, None, 1), "interest": (1, 1)})
        self.dead.append({"size": (3, 2), "pattern": (1, None, 1, 2, 1, 1), "interest": (1, 0)})

        self.dead.append({"size": (3, 3), "pattern": (2, 1, 1, 2, None, 1, 0, 2, 2), "interest": (1, 1)})
        self.dead.append({"size": (3, 3), "pattern": (0, 2, 2, 2, None, 1, 2, 1, 1), "interest": (1, 1)})
        self.dead.append({"size": (3, 3), "pattern": (2, 2, 1, 0, None, 1, 0, 2, 2), "interest": (1, 1)})
        self.dead.append({"size": (3, 3), "pattern": (0, 2, 2, 0, None, 1, 2, 2, 1), "interest": (1, 1)})

        self.prunepattern = (
            (1, -2), (-1, -1), (0, -1), (1, -1), (2, -1), (-1, 0), (0, 0), (1, 0), (-2, 1), (-1, 1), (0, 1), (1, 1),
            (-1, 2)
        )

    def extract(self, state, bridge, offset, marker):
        substate = list()
        index = 0
        pattern = bridge['pattern']
        for y in range(bridge['size'][1]):
            for x in range(bridge['size'][0]):
                statemarker = state[x + offset[0]][y + offset[1]]
                if pattern[index] == 2:
                    substate.append(2)
                elif statemarker == marker:
                    substate.append(1)
                elif statemarker is None:
                    substate.append(None)
                elif statemarker != marker and statemarker is not None:
                    substate.append(0)
                index += 1
        return tuple(substate)

    def search(self, board, marker, db):
        """
        Find patterns to be used as a feature for search
        :param board:
        :param marker:
        :return:
        """
        patterns = list()
        for pattern in db:
            for x in range(board.size - pattern['size'][0]):
                for y in range(board.size - pattern['size'][1]):
                    if self.extract(board.state, pattern, (x, y), marker) == pattern['pattern']:
                        patterns.append((x + pattern['interest'][0], y + pattern['interest'][1]))
        return patterns

    def findbridges(self, board, marker):
        return self.search(board, marker, self.bridges)

    def finddeadcells(self, board, marker):
        return self.search(board, marker, self.dead)

    def getpattern(self, board):
        moves = set()
        for pos, marker in board.markers.items():
            for x, y in self.prunepattern:
                if pos[0] + x >= 0 and pos[1] + y >= 0:
                    moves.add((pos[0] + x, pos[1] + y))
        if not moves:
            for x in range(board.size):
                for y in range(board.size):
                    moves.add((x, y))
        return moves
