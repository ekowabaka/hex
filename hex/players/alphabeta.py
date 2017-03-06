import math
import time
from hex import representation
from hex import patterns


class AlphaBeta(object):
    """
    Plain alpha-beta search agent.
    This agent uses the player flow heuristic to implement a classic alpha-beta search of gametree nodes to determine
    gameplay actions.
    """

    def __init__(self, board, marker):
        self.patternsearch = patterns.Search()
        self.size = board.size
        self.flows = dict()
        self.max = marker
        self.min = representation.BLACK_MARKER if marker == representation.WHITE_MARKER else representation.WHITE_MARKER
        self.maxdepth = 3
        self.nodes = 0
        self.stats = list()

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

    def getmove(self, board):
        self.nodes = 0
        start = time.time()
        move = self.alphabeta(board)
        self.stats.append({"nodes": self.nodes, "time": time.time() - start})
        return move['move']

    def evaluate(self, board, depth=1):
        raise "Implement the evaluation function"

    def alphabeta(self, board, depth=None, alpha=-float('inf'), beta=float('inf'), ismax=True):
        self.nodes += 1
        if depth is None:
            depth = self.maxdepth
        if depth == 0 or board.isend():
            return {'value': self.evaluate(board, depth)}

        playpattern = self.patternsearch.getpattern(board)
        deadcells = self.patternsearch.finddeadcells(board, self.max)
        for move in deadcells:
            playpattern.discard(move)

        bestmove = None

        if ismax:
            moves = board.getmoves(self.max)
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
            moves = board.getmoves(self.min)
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


class FlowAlphaBeta(AlphaBeta):
    def evaluate(self, board, depth=1):
        if board.isend():
            if board.winner == self.max:
                heuristic = 10 * (depth + 1)
            else:
                heuristic = 0
        else:
            maxflow = self.getflow(board.blackgraph if self.max == representation.BLACK_MARKER else board.whitegraph)
            minflow = self.getflow(board.whitegraph if self.min == representation.WHITE_MARKER else board.blackgraph)
            heuristic = math.log(maxflow / minflow if minflow > 0 else 0.01)
        return heuristic


class YReductionAlphaBeta(AlphaBeta):
    def evaluate(self, board, depth=1):
        ysize = board.size + board.size - 1
        yboard = list()
        for x in range(ysize):
            column = list()
            for y in range(ysize - x):
                if x < board.size and y < board.size:
                    state = board.state[x][y]
                    column.append(
                        -1 if state == self.min else 1 if state == self.max else 0)
                elif x >= board.size:
                    column.append(-1)
                elif y >= board.size:
                    column.append(1)
            yboard.append(column)

        for iteration in range(ysize, 0, -1):
            for y in range(iteration - 1):
                for x in range(iteration - 1 - y):
                    p1 = yboard[x][y]
                    p2 = yboard[x + 1][y]
                    p3 = yboard[x][y + 1]
                    yboard[x][y] = (p1 + p2 + p3 - p1 * p2 * p3) / 2

        return yboard[0][0]
