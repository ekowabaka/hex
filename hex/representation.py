import sys
import copy
import math

BLACK_MARKER = 0
WHITE_MARKER = 1


class Graph(object):
    def nodeid(self, x, y):
        return y * self.size + x

    def nodecoords(self, v):
        y = math.floor(v / self.size)
        return v % self.size, y

    def addedge(self, u, v):
        neighbors = set(self.children[u])
        neighbors.add(v)
        self.children[u] = frozenset(neighbors)
        parents = set(self.parents[v])
        parents.add(u)
        self.parents[v] = frozenset(parents)

    def getneighbors(self, v):
        return self.children[v]

    def getcoordneighbors(self, x, y):
        return self.coordinates[(x,y)]

    def getparents(self, v):
        return self.parents[v]

    def removevertex(self, v):
        neighbors = list(self.children[v].union(self.parents[v]))
        for i in range(-1, self.maxvertex + 1):
            if v in self.children[i]:
                items = set(self.children[i])
                items.remove(v)
                self.children[i] = frozenset(items)
            if v in self.parents[i]:
                items = set(self.parents[i])
                items.remove(v)
                self.parents[i] = frozenset(items)
        self.children[v] = set()
        self.parents[v] = set()
        return neighbors

    def clone(self):
        clone = Graph()
        clone.size = self.size
        clone.offsets = self.offsets
        clone.maxvertex = self.maxvertex
        clone.cmp = self.cmp
        clone.children = copy.copy(self.children)
        clone.parents = copy.copy(self.parents)
        clone.coordinates = self.coordinates
        return clone

    def __init__(self):
        self.size = None
        self.offsets = None
        self.maxvertex = None
        self.children = None
        self.parents = None
        self.cmp = None
        self.rank = list()
        self.coordinates = dict()

    def setup(self, size, cmp):
        self.size = size
        self.offsets = [-size, 1-size, -1, 1, size-1, size]
        self.maxvertex = size * size
        self.children = dict([(x, frozenset()) for x in range(-1, self.maxvertex + 1)])
        self.parents = dict([(x, frozenset()) for x in range(-1, self.maxvertex + 1)])
        self.cmp = cmp

        # Connect all the edges in the children representation
        for x in range(size):
            for y in range(size):
                node = self.nodeid(x, y)
                neighbors = [(x + offsetx, y + offsety) for offsetx, offsety in
                             [(-1, 0), (-1, +1), (0, -1), (0, 1), (1, -1), (1, 0)]
                             if 0 <= x + offsetx < size and 0 <= y + offsety < size]
                for neighbor in neighbors:
                    if cmp(neighbor, (x, y)):
                        neighbor = self.nodeid(neighbor[0], neighbor[1])
                        if neighbor not in self.children[node] and node not in self.children[neighbor]:
                            self.addedge(node, neighbor)

        for x in range(size):
            for y in range(size):
                for child in self.children[self.nodeid(x, y)].union(self.parents[self.nodeid(x, y)]):
                    if (x, y) not in self.coordinates:
                        self.coordinates[(x, y)] = list()
                    self.coordinates[(x, y)].append(self.nodecoords(child))

class Board(object):
    def __init__(self):
        self.state = ()
        self.blackgraph = None
        self.whitegraph = None
        self.markers = dict()
        self.size = None
        self.usegraphs = True
        self.winner = None

    def dfs(self, start, goals, graph, marker):
        stack = list()
        stack.append(start)
        seen = list()
        while stack:
            node = stack.pop()
            seen.append(node)
            for child in graph.getcoordneighbors(node[0], node[1]):
                if self.state[child[0]][child[1]] == marker:
                    if child in goals:
                        return True
                    if child not in seen:
                        stack.append(child)

    def isend(self):
        if self.usegraphs:
            if self.blackgraph.maxvertex in self.blackgraph.children[-1]:
                self.winner = BLACK_MARKER
                return True
            if self.whitegraph.maxvertex in self.whitegraph.children[-1]:
                self.winner = WHITE_MARKER
                return True
        else:
            for pos, marker in self.markers.items():
                if pos in [(x, 0) for x in range(self.size)] and self.state[pos[0]][pos[1]] == BLACK_MARKER:
                    if self.dfs(pos, [(x, self.size - 1) for x in range(self.size)], self.blackgraph, BLACK_MARKER):
                        self.winner = BLACK_MARKER
                        return True
                if pos in [(0, y) for y in range(self.size)] and self.state[pos[0]][pos[1]] == WHITE_MARKER:
                    if self.dfs(pos, [(self.size - 1, y) for y in range(self.size)], self.whitegraph, WHITE_MARKER):
                        self.winner = WHITE_MARKER
                        return True
        return False

    def setup(self, size=8, state=None):
        # Representation for current state of the board as a tuple
        self.state = tuple((None,) * size for i in range(size))
        self.blackgraph = Graph()
        self.blackgraph.setup(size, lambda u, v: True if u[1] > v[1] else u[0] > v[0] if u[1] == v[1] else False)
        self.whitegraph = Graph()
        self.whitegraph.setup(size, lambda u, v: True if u[0] > v[0] else u[1] > v[1] if u[0] == v[0] else False)
        self.size = size

        # Connect flow edges to children for players
        s = -1
        t = self.blackgraph.maxvertex
        for node in range(size):
            self.blackgraph.addedge(s, node)
            self.blackgraph.addedge(node + t - size, t)

            self.whitegraph.addedge(s, node * size)
            self.whitegraph.addedge((node + 1) * size - 1, t)

        # Rebuild the flow children if a new state was presented
        if state:
            for x in range(size):
                for y in range (size):
                    if state[x][y] is not None:
                        self.addmarker(x, y, state[x][y])

    def clone(self):
        clone = Board()
        clone.state = self.state
        clone.size = self.size
        clone.markers = copy.copy(self.markers)
        clone.usegraphs = self.usegraphs
        if self.usegraphs:
            clone.blackgraph = self.blackgraph.clone()
            clone.whitegraph = self.whitegraph.clone()
        else:
            clone.blackgraph = self.blackgraph
            clone.whitegraph = self.whitegraph
        return clone

    def getmoves(self, marker, withboards=True):
        moves = list()
        for x in range(self.size):
            for y in range(self.size):
                if self.state[x][y] is None:
                    if withboards:
                        move = self.clone()
                        move.addmarker(x, y, marker)
                        moves.append({"pos": (x, y), "board": move})
                    else:
                        moves.append((x, y))
        return moves

    def newcol(self, column, position, marker):
        column = list(column)
        column[position] = marker
        return tuple(column)

    def addmarker(self, x, y, marker):
        self.state = tuple(self.state[i] if i != x else self.newcol(self.state[i], y, marker) for i in range(len(self.state)))
        self.markers[(x, y)] = marker
        if self.usegraphs:
            self.modifygraph(x, y, self.blackgraph, marker, BLACK_MARKER)
            self.modifygraph(x, y, self.whitegraph, marker, WHITE_MARKER)

    def getflatstate(self):
        return {i: self.state[int(i/self.size)][i % self.size] for i in range(self.blackgraph.maxvertex)}

    def modifygraph(self, x, y, graph, marker, state):
        nodeid = graph.nodeid(x, y)
        neighbors = graph.removevertex(nodeid)
        if marker == state:
            for u in neighbors:
                for v in neighbors:
                    if u == v:
                        continue
                    if graph.maxvertex > u > -1:
                        ux = u % graph.size
                        uy = int(u / graph.size)
                    else:
                        ux = u
                        uy = u

                    if graph.maxvertex > v > -1:
                        vx = v % graph.size
                        vy = int(v / graph.size)
                    else:
                        vx = v
                        vy = v

                    if graph.cmp((ux, uy), (vx, vy)):
                        graph.addedge(v, u)
    def draw(self):
        indent = 0
        sys.stdout.write('       ')
        for alpha in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            sys.stdout.write(alpha + '  ')
        sys.stdout.write('\n       ')
        for alpha in range(self.size):
            sys.stdout.write('B  ')
        print()
        for y in range(self.size):

            sys.stdout.write(str(y+1) + '  W   ')
            for x in range(self.size):
                marker = '.'
                if self.state[x][y] == BLACK_MARKER:
                    marker = 'B'
                elif self.state[x][y] == WHITE_MARKER:
                    marker = 'W'
                sys.stdout.write(marker + '  ')
            sys.stdout.write("\n")
            indent += 1
            sys.stdout.write('  ' * indent)

        print()
