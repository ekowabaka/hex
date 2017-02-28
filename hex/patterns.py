class Search(object):
    def __init__(self):
        self.bridges = list()
        self.bridges.append({"size":(2,2), "pattern":(1,0,0,1)})
        self.bridges.append({"size":(2,3), "pattern":(0,1,0,0,1,0)})
        self.bridges.append({"size":(3,2), "pattern":(0,0,1,1,0,0)})

    def extract(self, state, window, offset, marker):
        substate  = list()
        for x in range(window[0]):
            for y in range(window[1]):
                substate.append(1 if state[x + offset[0]][y + offset[1]] == marker else 0)
        return tuple(substate)

    def findbridges(self, board, marker):
        """
        Find possible bridges so search can be weighed towards boards that have more bridges
        :param board:
        :param marker:
        :return:
        """
        for bridge in self.bridges:
            for x in range(board.size - bridge['size'][0]):
                for y in range(board.size - bridge['size'][1]):
                    if self.extract(board.state, bridge['size'], (x,y), marker) == bridge['pattern']:
                        board.draw()
                        print(x,y,bridge['pattern'],marker)



