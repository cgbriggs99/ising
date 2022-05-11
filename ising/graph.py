#!/usr/bin/python3

"""
ising.graph

Contains definitions for graphs, as well as a couple functions to test them.
"""

try:
    from . import despats
except ImportError:
    import despats


class Copyable:
    """
Defines an object that is copyable.
"""

    def copy(self):
        """
Copy an object.
"""
        raise NotImplementedError(f"Copy not implemented yet for {type(self)}.")

    @staticmethod
    def iscopyable(obj):
        """
Returns whether an object is copyable.
"""
        return hasattr(obj, "copy")


class Vertex(Copyable):
    """
Represents a vertex in a graph.
"""

    def __init__(self, data, index):
        self._data = data
        self._index = index

    def getdata(self):
        """
Gets the data at a vertex.
"""
        return self._data

    def setdata(self, data):
        """
Sets the data at a vertex.
"""
        self._data = data
        return data

    def getindex(self):
        """"
Gets the unique index of the vertex.
"""
        return self._index

    def _setindex(self, index: int):
        self._index = index
        return index

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return (self is other) or (
                self._data == other._data and self._index == other._index
            )
        if isinstance(self._index, type(other)) or isinstance(other, type(self._index)):
            return self._index == other
        return False

    def copy(self):
        if Copyable.iscopyable(self._data):
            out = Vertex(self._data.copy(), self.getindex())
            return out
        return Vertex(self._data, self.getindex())

    def __str__(self):
        if self.getdata() is not None:
            return f"({self.getindex()}: {self.getdata()})"
        return f"({self.getindex()})"

    def __hash__(self):
        return self.getindex()


class Edge(Copyable):
    """
Represents an edge in a graph.
"""

    def __init__(self, index, start, end, length=1):
        self._start = start
        self._end = end
        self._length = length
        self._index = index

    def getstart(self):
        """
Returns the beginning node of the edge.
"""
        return self._start

    def getend(self):
        """
Returns the ending node of the edge.
"""
        return self._end

    def getlength(self):
        """
Returns the length of the edge.
"""
        return self._length

    def setstart(self, vert):
        """
Sets the starting node of the edge.
"""
        self._start = vert
        return vert

    def setend(self, vert):
        """
Sets the ending node of the edge.
"""
        self._end = vert
        return vert

    def setlength(self, length):
        """
Sets the length of the edge.
"""
        self._length = length
        return length

    def getindex(self):
        """
Gets the unique index of the edge.
"""
        return self._index

    def _setindex(self, index):
        self._index = index
        return self._index

    def cantraverse(self, vert):
        """
Returns whether an edge can be traversed from a given vertex.
"""
        return self.getstart() == vert

    def traverse(self, vert):
        """
Tries to traverse an edge from a vertex.
"""
        assert self.getstart() == vert
        return (self.getend(), self.getlength())

    def __eq__(self, other):
        if isinstance(other, Edge):
            return (self is other) or (
                self._length == other._length
                and self._start == other._start
                and self._end == other._end
            )
        if isinstance(self._index, type(other)) or isinstance(other, type(self._index)):
            return self.getindex() == other
        return False

    def copy(self):
        """
Copies an edge.
"""
        if Copyable.iscopyable(self._length):
            return Edge(
                self.getindex(),
                self._start.copy(),
                self._end.copy(),
                self._length.copy(),
            )
        return Edge(self.getindex(), self._start.copy(), self._end.copy(), self._length)

    def __str__(self):
        if self.getlength() is not None:
            return (
                f"[{self.getindex()} : "
                + f"{self.getstart()} -> {self.getend()} ({self.getlength()})]"
            )
        return f"[{self.getindex()} : " + f"{self.getstart()} -> {self.getend()}]"

    def __hash__(self):
        return self.getindex()


class UndirectedEdge(Edge):
    """
Represents an undirected edge.
"""

    def cantraverse(self, vert):
        return self.getstart() == vert or self.getend() == vert

    def traverse(self, vert):
        if self.getstart() == vert:
            return (self.getend(), self.getlength())
        if self.getend() == vert:
            return (self.getstart(), self.getlength())
        raise Exception("Vertex not the start or end of the edge.")

    def copy(self):
        if Copyable.iscopyable(self.getlength()):
            return UndirectedEdge(
                self.getindex(),
                self.getstart().copy(),
                self.getend().copy(),
                self.getlength().copy(),
            )
        return UndirectedEdge(
            self.getindex(),
            self.getstart().copy(),
            self.getend().copy(),
            self.getlength(),
        )

    def __eq__(self, other):
        if isinstance(other, UndirectedEdge):
            return (self is other) or (
                self.getlength() == other.getlength()
                and (
                    self.getstart() == other.getstart()
                    and self.getend() == other.getend()
                )
                or (
                    self.getstart() == other.getend()
                    and self.getend() == other.getstart()
                )
            )
        if isinstance(self.getindex(), type(other)) or isinstance(
            other, type(self.getindex())
        ):
            return self.getindex() == other
        return False

    def __str__(self):
        if self.getlength() is not None:
            return (
                f"[{self.getindex()} : "
                + f"{self.getstart()} <-> {self.getend()} ({self.getlength()})]"
            )
        return f"[{self.getindex()} : " + f"{self.getstart()} <-> {self.getend()}]"


class VertexFactory(despats.Singleton):
    """
Represents a vertex factory.
"""

    def __init__(self):
        self._index = 0

    def makevertex(self, data=None):
        """
Makes a vertex.
"""
        out = Vertex(data, self._index)
        self._index += 1
        return out

    def makevertex_list(self, nverts: int, data=None):
        """
Makes several vertices.
"""
        if hasattr(data, "__iter__"):
            return [self.makevertex(d) for d, _ in zip(data, range(nverts))]
        return [self.makevertex(data) for _ in range(nverts)]


class EdgeFactory(despats.Singleton):  # pylint: disable=too-few-public-methods
    """
Represents an edge factory.
"""

    def __init__(self):
        self._index = 0

    def makeedge(self, start, end, length=1, directed=True):
        """
Makes an edge.
"""
        if directed:
            out = Edge(self._index, start, end, length)
            self._index += 1
            return out
        out = UndirectedEdge(self._index, start, end, length)
        self._index += 1
        return out


# Base representation.
class Graph:
    """
Represents a general graph.
"""

    def __init__(self, verts, edges):
        if verts is None:
            self._verts = []
        else:
            self._verts = verts
        if edges is None:
            self._edges = []
        else:
            self._edges = edges

    def getverts(self):
        """
Returns the list of vertices.
"""
        return self._verts

    def getvert(self, index):
        """
Gets a vertex with the specified index.
"""
        for vert in self.getverts():
            if vert.getindex() == index or vert == index:
                return vert
        return None

    def getedges(self):
        """
Returns the list of edges.
"""
        return self._edges

    def getedge(self, index, cutoff=1e-6):
        """
Gets an edge with a specified start and end indices, or a specified index.
"""
        if hasattr(index, "__iter__"):
            for edg in self.getedges():
                if isinstance(edg, UndirectedEdge):
                    if (
                        (edg.getstart() == index[0] and edg.getend() == index[1])
                        or (edg.getstart() == index[1] and edg.getend() == index[0])
                    ) and (
                        (len(index) == 3 and abs(edg.getlength() - index[2]) < cutoff)
                        or len(index) != 3
                    ):
                        return edg
                else:
                    if (edg.getstart() == index[0] and edg.getend() == index[1]) and (
                        (len(index) == 3 and abs(edg.getlength() - index[2]) < cutoff)
                        or len(index) != 3
                    ):
                        return edg
        else:
            for edg in self.getedges():
                if edg.getindex() == index:
                    return edg
        return None

    def addverts(self, vert):
        """
Can do single vertices or a collection of vertices.
"""
        if hasattr(vert, "__iter__"):
            assert all(map(lambda x: isinstance(x, Vertex), vert))
            for ver in vert:
                self._verts.append(ver)
        else:
            self._verts.append(vert)
        return self._verts

    def addedges(self, edge):
        """
Can do single edges or a collection of edges.
"""
        if hasattr(edge, "__iter__"):
            assert all(map(lambda x: isinstance(x, Edge), edge))
            for edg in edge:
                self._edges.append(edg)
        elif isinstance(edge, Edge):
            self._edges.append(edge)
        return self._edges

    def hasvertex(self, vert):
        """
Returns whether a vertex is in the graph.
"""
        return vert in self.getverts()

    def hasedge(self, edge):
        """
Returns whether an edge is in the graph.
"""
        return edge in self.getedges()

    def getneighbors(self, vert):
        """
Returns the neighbors of a vertex.
"""
        neigh = []
        for edg in self.getedges():
            if edg.cantraverse(vert):
                neigh.append(
                    tuple(list(edg.traverse(vert)) + [isinstance(edg, UndirectedEdge)])
                )
        return neigh

    def __str__(self):
        return "{" + str(self.getedges()) + ", " + str(self.getverts()) + "}"


def dijkstra(graph: Graph, start: Vertex, end: Vertex):
    """
Dijkstra's shortest path. Useful for testing the graph implementation.
"""
    visited = {start: (0, None)}
    openset = [(start, n) for n in graph.getneighbors(start)]

    while len(openset) > 0:
        vert = openset.pop()
        dist = visited[vert[0]][0] + vert[1][1]
        if (vert[1][0] in visited and visited[vert[1][0]][0] > dist) or vert[1][
            0
        ] not in visited:
            # Update if vertex is new, or if the distance it has is shorter.
            visited[vert[1][0]] = (dist, vert[0])
            # Only generate neighbors if it was added.
            openset = openset + [
                (vert[1][0], n) for n in graph.getneighbors(vert[1][0])
            ]
    if end in visited:
        verts = []
        edges = []
        curr = end
        while curr != start:
            verts.append(curr)
            edges.append(
                graph.getedge(
                    (
                        visited[curr][1],
                        curr,
                        visited[curr][0] - visited[visited[curr][1]][0],
                    )
                )
            )
            curr = visited[curr][1]

        print(Graph(verts, edges))
        return Graph(verts, edges)
    return None
