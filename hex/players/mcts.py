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

    def __init__(self):
        self.states = None

    def getmove(self, board):
        self.mcts(board)
        action = max([x.state for x in self.states[board.state].children], key=lambda x: self.states[x].q)
        return self.states[action].move

    def mcts(self, board):
        self.states = dict()
        self.states[board.state] = MonteCarloState(moves=board.getmoves(representation.BLACK_MARKER))
        terminated = False
        start = time.time()

        while not terminated:
            if time.time() - start > 20:
                terminated = True
            newboard = self.treepolicy(board)
            if not newboard:
                continue
            state = newboard.state
            value = self.defaultpolicy(newboard)
            self.backup(state, value)

    def treepolicy(self, root):
        board = root
        while not board.isend():
            if len(self.states[board.state].moves) > 0:
                return self.expand(board)
            else:
                board = self.bestchild(board)

    def expand(self, board):
        newstate = self.states[board.state].moves.pop()
        newboard = newstate['board']
        markers = [representation.WHITE_MARKER, representation.BLACK_MARKER]
        depth = self.states[board.state].depth + 1
        moves = newboard.getmoves(markers[depth % 2])
        self.states[newboard.state] = MonteCarloState(moves=moves, parent=board.state)
        self.states[newboard.state].move = newstate['pos']
        self.states[newboard.state].depth = depth
        return newboard

    def defaultpolicy(self, board):
        # Implement full playout of game state
        markers = [representation.BLACK_MARKER, representation.WHITE_MARKER]
        turn = 0
        playboard = board.clone()
        while not playboard.isend():
            moves = playboard.getmoves(markers[turn], withboards=False)
            move = moves[random.randrange(len(moves))]
            playboard.addmarker(move[0], move[1], markers[turn])
            turn = int(not turn)
        return 1 if playboard.iswin() else -1

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

