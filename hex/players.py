from hex import representation
from hex import patterns
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


class MonteCarloUCT(object):
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
        # Build a dictionary with state as key and a tuple of (board, q) as values
        children = {x.state:  (x, self.states[x.state].q/self.states[x.state].n + c * math.sqrt((2 * math.log(self.states[board.state].n, math.e))) / self.states[x.state].n) for x in self.states[board.state].children}
        best = max(children.items(), key=lambda x: x[1][1])[0]
        return children[best][0]

class AlphaBeta(object):
    """
    Plain alpha-beta search agent.
    This agent uses the player flow heuristic to implement a classic alpha-beta search of gametree nodes to determine
    gameplay actions.
    """

    def __init__(self, board):
        self.patternsearch = patterns.Search()
        self.size = board.size
        self.flows = dict()

    def getflow(self, graph, node=None):
        if node is None:
            self.flows = dict()
            node = graph.maxvertex
        if node == -1:
            return float('inf')
        flow = 0
        for parent in graph.getparents(node):
            if parent not in self.flows:
                self.flows[parent] = self.getflow(graph, parent)
            flow += self.flows[parent]

        numchildren = len(graph.children[node])

        if flow > numchildren and node != graph.maxvertex:
            flow = 1
        elif node != graph.maxvertex:
            flow /= numchildren

        return flow
        # flow = 0
        # for node in range(-1, graph.maxvertex + 1):
        #     for child in graph.getneighbors(node):
        #
        #         flow += 1
        # return flow

    def getmove(self, board):
        move = self.alphabeta(board)
        return move['move']

    def evaluate(self, board, depth=1):
        if board.iswin():
            heuristic = 10 * (depth + 1)
        elif board.islose():
            heuristic = 0
        else:
            whiteflow = self.getflow(board.whitegraph)
            blackflow = self.getflow(board.blackgraph)
            # board.draw()
            # print(blackflow, whiteflow)
            heuristic = math.log(blackflow / whiteflow)


        # heuristic += (self.patternsearch.countbridges(board, representation.BLACK_MARKER) * 2)

        # ysize = board.size + board.size - 1
        # yboard = list()
        # for x in range(ysize):
        #     column = list()
        #     for y in range(ysize-x):
        #         if x < board.size and y < board.size:
        #             state = board.state[x][y]
        #             column.append(-1 if state == representation.WHITE_MARKER else 1 if state == representation.BLACK_MARKER else 0)
        #         elif x >= board.size:
        #             column.append(-1)
        #         elif y >= board.size:
        #             column.append(1)
        #     yboard.append(column)
        #
        # for iteration in range(ysize, 0, -1):
        #     for y in range(iteration - 1):
        #         for x in range(iteration - 1 - y):
        #             p1 = yboard[x][y]
        #             p2 = yboard[x+1][y]
        #             p3 = yboard[x][y+1]
        #             yboard[x][y] = (p1 + p2 + p3 - p1 * p2 * p3) / 2
        #
        # heuristic = yboard[0][0]

        return heuristic

    def alphabeta(self, board, depth=4, alpha=-float('inf'), beta=float('inf'), ismax=True):
        if depth == 0 or board.iswin() or board.islose():
            return {'value': self.evaluate(board, depth)}

        playpattern = self.patternsearch.getpattern(board)
        bestmove = None

        if ismax:
            moves = board.getmoves(representation.BLACK_MARKER)
            for move in moves:
                if move['pos'] not in playpattern:
                    continue
                value = self.alphabeta(move['board'], depth - 1, alpha, beta, False)
                if value['value'] > alpha:
                    bestmove = move['pos']
                    alpha = value['value']
                if alpha >= beta:
                    break
            return {'value': alpha, 'move': bestmove}
        else:
            moves = board.getmoves(representation.WHITE_MARKER)
            for move in moves:
                if move['pos'] not in playpattern:
                    continue
                value = self.alphabeta(move['board'], depth - 1, alpha, beta, True)
                if value['value'] < beta:
                    beta = value['value']
                    bestmove = move['pos']
                if beta <= alpha:
                    break
            return {'value': beta, 'move': bestmove}

