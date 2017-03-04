from hex import representation
import math
import random
import time


class MonteCarloState(object):
    def __init__(self, parent=None, moves=[]):
        self.n = 0
        self.q = 0
        self.parent = parent
        self.move = None
        self.moves = moves
        self.depth = 0
        if len(moves) > 0:
            self.children = list([x["board"] for x in moves])


class PureRandomUCT(object):
    """
    A pure random MonteCarlo search tree.
    """

    def __init__(self, marker):
        self.max = marker
        self.min = representation.BLACK_MARKER if marker == representation.WHITE_MARKER else representation.WHITE_MARKER
        self.states = None

    def getmove(self, board):
        self.mcts(board)
        action = max([x.state for x in self.states[board.state].children], key=lambda x: self.states[x].q)
        return self.states[action].move

    def mcts(self, board):
        self.states = dict()
        self.states[board.state] = MonteCarloState(moves=board.getmoves(self.max))
        terminated = False
        start = time.time()
        iterations = 0

        while not terminated:
            if time.time() - start > 90:
                terminated = True
            newboard = self.treepolicy(board)
            if not newboard:
                continue
            state = newboard.state
            value = self.defaultpolicy(newboard)
            self.backup(state, value)
            iterations += 1

        print("Iterations:", iterations)


    def treepolicy(self, root):
        board = root
        while not board.isend():
            if len(self.states[board.state].moves) > 0:
                return self.expand(board)
            else:
                board = self.bestchild(board)

    def expand(self, board):
        moveindex = random.randrange(len(self.states[board.state].moves))
        newstate = self.states[board.state].moves[moveindex]
        del self.states[board.state].moves[moveindex]
        newboard = newstate['board']
        markers = [self.min, self.max]
        depth = self.states[board.state].depth + 1
        moves = newboard.getmoves(markers[depth % 2])
        self.states[newboard.state] = MonteCarloState(moves=moves, parent=board.state)
        self.states[newboard.state].move = newstate['pos']
        self.states[newboard.state].depth = depth
        return newboard

    def defaultpolicy(self, board):
        # Implement full playout of game state
        markers = [self.max, self.min]
        turn = self.states[board.state].depth % 2
        playboard = board.clone()
        while not playboard.isend():
            moves = playboard.getmoves(markers[turn], withboards=False)
            move = moves[random.randrange(len(moves))]
            playboard.addmarker(move[0], move[1], markers[turn])
            turn = int(not turn)
        return 1 if playboard.getwin() == self.max else -1

    def backup(self, state, value):
        while state:
            self.states[state].n += 1
            self.states[state].q += value
            value = -value
            state = self.states[state].parent

    def bestchild(self, board):
        c = 0.707106
        children = {x.state:  (x, self.states[x.state].q/self.states[x.state].n + c * math.sqrt((2 * math.log(self.states[board.state].n, math.e))) / self.states[x.state].n) for x in self.states[board.state].children}
        best = max(children.items(), key=lambda x: x[1][1])[0]
        return children[best][0]

