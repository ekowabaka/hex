from hex import representation, patterns
import math
import random
import time


class MonteCarloState(object):
    def __init__(self, parent=None, moves=None):
        self.n = 0
        self.q = 0
        self.parent = parent
        self.move = None
        self.moves = moves
        self.depth = 0
        self.children = list()
        if moves is not None: self.updatechildren()

    def updatechildren(self):
        if len(self.moves) > 0:
            self.children = list([x["board"] for x in self.moves])


class PureRandomUCT(object):
    """
    A pure random MonteCarlo search tree.
    """

    def __init__(self, marker):
        self.max = marker
        self.min = representation.BLACK_MARKER if marker == representation.WHITE_MARKER else representation.WHITE_MARKER
        self.states = None
        self.stats = list()
        self.iterations = 0
        self.maxtime = 60
        self.selection = 'n'
        random.seed()

    def getmove(self, board):
        self.iterations = 0
        self.mcts(board)

        if self.selection == 'n':
            action = max([x.state for x in self.states[board.state].children], key=lambda x: self.states[x].n)
        else:
            action = max([x.state for x in self.states[board.state].children], key=lambda x: self.states[x].q)

        self.stats.append({"nodes":len(self.states), "iterations": self.iterations})
        return self.states[action].move

    def getmoves(self, board):
        moves = board.getmoves(self.max)
        moves.sort(key=lambda x: random.random())
        return moves

    def mcts(self, board):
        self.states = dict()
        board = board.clone()
        board.usegraphs = False
        moves = self.getmoves(board)
        self.states[board.state] = MonteCarloState(moves=moves)
        terminated = False
        start = time.time()

        while not terminated:
            if time.time() - start > self.maxtime:
                terminated = True
            newboard = self.treepolicy(board)
            if not newboard:
                continue
            state = newboard.state
            value = self.defaultpolicy(newboard)
            self.backup(state, value)
            self.iterations += 1

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
        markers = [self.min, self.max]
        depth = self.states[board.state].depth + 1
        moves = newboard.getmoves(markers[depth % 2])
        moves.sort(key=lambda x: random.random())
        self.states[newboard.state] = MonteCarloState(moves=moves, parent=board.state)
        self.states[newboard.state].move = newstate['pos']
        self.states[newboard.state].depth = depth
        return newboard

    def defaultpolicy(self, board):
        # Implement full playout of game state
        markers = [self.max, self.min]
        turn = self.states[board.state].depth % 2
        playboard = board.clone()
        moves = playboard.getmoves(markers[turn], withboards=False)
        moves.sort(key=lambda x:random.random())

        while True:
            if len(moves) == 0:
                break
            move = moves.pop()
            playboard.addmarker(move[0], move[1], markers[turn])
            turn = int(not turn)
        playboard.isend()
        value = 1 if playboard.winner == self.max else -1

        return value

    def backup(self, state, value):
        while state:
            self.states[state].n += 1
            self.states[state].q += value
            value = -value
            state = self.states[state].parent

    def bestchild(self, board):
        c = 0.7
        maximum = float('-inf')
        best = None
        for x in self.states[board.state].children:
            rating = self.states[x.state].q / self.states[
                x.state].n + c * math.sqrt((2 * math.log(self.states[board.state].n))) / self.states[x.state].n
            if best is None:
                best = x
            if rating > maximum:
                maximum = rating
                best = x
        return best


class ExtendedMCTS(PureRandomUCT):

    def __init__(self, marker):
        PureRandomUCT.__init__(self, marker)
        self.patterns = patterns.Search()

    def getmoves(self, board):
        moves = list()
        boardmoves = board.getmoves(self.max)
        goodmoves = self.patterns.getpattern(board)

        for move in boardmoves:
            if move['pos'] in goodmoves:
                moves.append(move)

        moves.sort(key=lambda x: random.random())
        return moves


    def treepolicy(self, root):
        board = root
        while not board.isend():
            #board.draw()
            if self.states[board.state].moves is None:
                markers = [self.min, self.max]
                moves = board.getmoves(markers[self.states[board.state].depth % 2])
                moves.sort(key=lambda x: random.random())
                self.states[board.state].moves = moves
                self.states[board.state].updatechildren()
            if len(self.states[board.state].moves) > 0:
                return self.expand(board)
            else:
                board = self.bestchild(board)

    def defaultpolicy(self, board):
        # Implement full playout of game state
        markers = [self.max, self.min]
        states = [[], []]
        turn = self.states[board.state].depth % 2
        depth = self.states[board.state].depth
        playboard = board.clone()
        moves = playboard.getmoves(markers[turn], withboards=False)
        moves.sort(key=lambda x:random.random())

        while True:
            if len(moves) == 0:
                break

            parent = playboard.state
            bridges = self.patterns.findbridges(playboard, turn)
            if len(bridges) > 0:
                move = bridges.pop()
                moves.remove(move)
            else:
                move = moves.pop()
            playboard.addmarker(move[0], move[1], markers[turn])
            depth += 1
            if playboard.state not in self.states:
                self.states[playboard.state] = MonteCarloState(parent=parent)
                self.states[playboard.state].move = move
                self.states[playboard.state].depth = depth
                self.states[parent].children.append(playboard.clone())
            states[turn].append(playboard.state)
            turn = int(not turn)
        playboard.isend()
        value = 1 if playboard.winner == self.max else -1

        # Propagate AMAF Values
        for state in states[0]:
            self.states[state].n += 1
            self.states[state].q += value

        for state in states[1]:
            self.states[state].n += 1
            self.states[state].q += -value

        return value
