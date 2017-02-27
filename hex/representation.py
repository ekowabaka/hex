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

        # Connect flow edges to graph for players
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

class Carrier(object):
    def __init__(self, carrier):
        self.new = True
        self.carrier = carrier

class HSearch(object):
    def __init__(self, graph):
        self.graph = graph

    def getneighbors(self, vertex, state, marker):
        vertices = self.graph.getneighbors(vertex)
        neighbors = []
        for v in vertices:
            if state[v] == marker:
                #print(k,v)
                neighbors.append(v)
        return neighbors

    def getgroups(self, state, marker):
        groups = list()
        added = False
        for i in range(-1, self.graph.maxvertex+1):
            if state[i] is None:
                groups.append({i})
                continue
            elif state[i] == marker:
                for group in groups:
                    if i in group:
                        group.update(self.getneighbors(i, state, marker))
                        added = True
                        break
                if not added:
                    group = set()
                    group.add(i)
                    group.update(self.getneighbors(i, state, marker))
                    groups.append(group)
        return groups

    def hasnew(self,c):
        for key, carriers in c.items():
            for carrier in carriers:
                if carrier.new:
                    return True
        return False

    def run(self, board, marker):
        # Group all the markers and build a list of markers for connectivity testing
        state = board.getflatstate()
        state[-1] = marker
        state[self.graph.maxvertex] = marker
        g = self.getgroups(state, marker)
        c = dict()
        newc = list()
        sc = dict()

        for g1 in g:
            g1 = frozenset(g1)
            for g2 in g:
                g2 = frozenset(g2)
                if g1 == g2:
                    continue
                key = frozenset([g1, g2])
                if key in c:
                    continue
                c[key] = list()
                sc[key] = list()
                for v1 in g1:
                    for v2 in g2:
                        if v1 in self.graph.getneighbors(v2) or v2 in self.graph.getneighbors(v1):
                            c[key].append(Carrier({None}))

        while self.hasnew(c):
            for _g in g:
                _g = frozenset(_g)
                _gl = list(_g)
                for g1 in g:
                    g1 = frozenset(g1)
                    g1l = list(g1)
                    for g2 in g:
                        g2 = frozenset(g2)
                        g2l = list(g2)
                        if g1 == g2:
                            continue
                        g1g = frozenset([g1, _g])
                        g2g = frozenset([g2, _g])

                        if g1g not in c: continue
                        if g2g not in c: continue
                        if state[_gl[0]] == BLACK_MARKER and (state[g1l[0]] is not None or state[g2l[0]] is not None):
                            continue
                        if len(c[g1g]) == 0: continue
                        if len(c[g2g]) == 0: continue

                        for c1 in c[g1g]:
                            for c2 in c[g2g]:
                                if not c1.new and not c2.new:
                                    continue
                                c1.new = False
                                c2.new = False
                                c1s = c1.carrier
                                c2s = c2.carrier

                                if len(c1s.intersection(c2s)) > 0: continue
                                if c1.issubset(g2): continue
                                if c2.issubset(g1): continue

                                if state[_g[0]] == BLACK_MARKER:
                                    c[frozenset([g1, g2])] = Carrier(c1s.union(c2s))
                                else:
                                    newsc = g1.union(c1s).union(c2s)
        #print('done')



        # Build lists of connections with nearest neighbors