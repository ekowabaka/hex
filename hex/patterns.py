class Search(object):
    def __init__(self):
        self.bridges = list()
        self.bridges.append({"size": (2, 2), "pattern": (1, None, None, 1), "offset": 0})
        self.bridges.append({"size": (2, 3), "pattern": (1, None, None, 1), "offset": 1})
        self.bridges.append({"size": (3, 2), "pattern": (None, 1, 1, None), "offset": 1})

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
        Find possible bridges so search can be weighed towards boards that have more bridges
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
