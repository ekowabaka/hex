from collections import deque
from hex import representation
import math


class NetworkFlow(object):

    def __init__(self, size):
        self.size = size

    def getflow(self, graph):
        flow = 0
        for node in range(-1, graph.maxvertex + 1):
            for child in graph.getneighbors(node):
                flow += 1
        return flow

    def getmove(self, board):
        move = self.alphabeta(board)
        return move['move']

    def evaluate(self, board, depth=1):
        whiteflow = self.getflow(board.whitegraph)
        blackflow = self.getflow(board.blackgraph)
        heuristic = math.log(blackflow / whiteflow)
        if board.iswin():
            heuristic += 10 * (depth + 1)
        if board.islose():
            heuristic -= 10 * (depth + 1)
        return heuristic

    def alphabeta(self, board, depth=5, alpha=-float('inf'), beta=float('inf'), ismax=True):
        if depth == 0 or board.iswin() or board.islose():
            return {'value': self.evaluate(board, depth)}

        bestmove = None

        if ismax:
            moves = board.getmoves(representation.BLACK_MARKER)
            for move in moves:
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
                value = self.alphabeta(move['board'], depth - 1, alpha, beta, True)
                if value['value'] < beta:
                    beta = value['value']
                    bestmove = move['pos']
                if beta <= alpha:
                    break
            return {'value': beta, 'move': bestmove}
