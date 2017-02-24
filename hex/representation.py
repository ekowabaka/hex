import sys
import copy

BLACK_MARKER = 0
WHITE_MARKER = 1

class Graph(object):
    def nodeid(self, x, y):
        return y * self.size + x

    def addedge(self, u, v):
        neighbors = set(self.graph[u])
        neighbors.add(v)
        self.graph[u] = frozenset(neighbors)

    def getneighbors(self, v):
        return self.graph[v]

    def removevertex(self, v):
        neighbors = list(self.graph[v])
        for i in range(-1, self.maxvertex + 1):
            if v in self.graph[i]:
                neighbors.append(i)
                items = set(self.graph[i])
                items.remove(v)
                self.graph[i] = frozenset(items)
        self.graph[v] = set()
        return neighbors

    def clone(self):
        clone = Graph()
        clone.size = self.size
        clone.offsets = self.offsets
        clone.maxvertex = self.maxvertex
        clone.cmp = self.cmp
        clone.graph = copy.copy(self.graph)
        return clone

    def __init__(self):
        self.size = None
        self.offsets = None
        self.maxvertex = None
        self.graph = None
        self.cmp = None

    def setup(self, size, cmp):
        self.size = size
        self.offsets = [-size, 1-size, -1, 1, size-1, size]
        self.maxvertex = size * size
        self.graph = dict([(x, frozenset()) for x in range(-1, self.maxvertex+1)])
        self.cmp = cmp
        # Connect all the edges in the graph representation
        for x in range(size):
            for y in range(size):
                node = self.nodeid(x, y)
                neighbors = [(x + offsetx, y + offsety) for offsetx, offsety in
                             [(-1, 0), (-1, +1), (0, -1), (0, 1), (1, -1), (1, 0)]
                             if 0 <= x + offsetx < size and 0 <= y + offsety < size]
                for neighbor in neighbors:
                    if cmp(neighbor, (x, y)):
                        neighbor = self.nodeid(neighbor[0], neighbor[1])
                        if neighbor not in self.graph[node] and node not in self.graph[neighbor]:
                            self.addedge(node, neighbor)

class Board(object):
    def __init__(self):
        self.state = ()
        self.blackgraph = None
        self.whitegraph = None
        self.size = None

    def iswin(self):
        if self.blackgraph.maxvertex in self.blackgraph.graph[-1]:
            return True

    def islose(self):
        if self.whitegraph.maxvertex in self.whitegraph.graph[-1]:
            return True

    def isend(self):
        return self.iswin() or self.islose()

    def setup(self, size=8, state=None):
        # Representation for current state of the board as a tuple
        self.state = tuple((None,) * size for i in range(size))
        self.blackgraph = Graph()
        self.blackgraph.setup(size, lambda u, v: True if u[1] > v[1] else u[0] > v[0] if u[1] == v[1] else False)
        self.whitegraph = Graph()
        self.whitegraph.setup(size, lambda u, v: True if u[0] > v[0] else u[1] > v[1] if u[0] == v[0] else False)
        self.size = size

        # Connect flow edges to graph for black player
        s = -1
        t = self.blackgraph.maxvertex
        for node in range(size):
            self.blackgraph.addedge(s, node)
            self.blackgraph.addedge(node + t - size, t)

            self.whitegraph.addedge(s, node * size)
            self.whitegraph.addedge((node + 1) * size - 1, t)

        # Rebuild the flow graph if a new state was presented
        if state:
            for x in range(size):
                for y in range (size):
                    if state[x][y] is not None:
                        self.addmarker(x, y, state[x][y])

    def clone(self):
        clone = Board()
        clone.state = self.state
        clone.blackgraph = self.blackgraph.clone()
        clone.whitegraph = self.whitegraph.clone()
        clone.size = self.size
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
        self.modifygraph(x, y, self.blackgraph, marker, BLACK_MARKER)
        self.modifygraph(x, y, self.whitegraph, marker, WHITE_MARKER)

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
        i = 0
        size = len(self.state)
        for y in range(size):
            for x in range(size):
                marker = '.'
                if self.state[x][y] == BLACK_MARKER:
                    marker = '0'
                elif self.state[x][y] == WHITE_MARKER:
                    marker = 'X'
                sys.stdout.write(marker + ' ')
                i+=1
            sys.stdout.write("\n")
            indent += 1
            sys.stdout.write(' ' * indent)