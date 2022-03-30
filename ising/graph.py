#!/usr/bin/python3

try :
    from . import despats
except ImportError :
    import despats

class Copyable :
    def copy(self) :
        raise NotImplemented(f"Copy not implemented yet for {type(self)}.")

    @staticmethod
    def iscopyable(obj) :
        return hasattr(obj, "copy")

class Vertex(Copyable) :
    def __init__(self, data, index) :
        self.__data = data
        self.__index = index

    def getdata(self) :
        return self.__data
    
    def setdata(self, data) :
        self.__data = data
        return data

    def getindex(self) :
        return self.__index

    def _setindex(self, index : int) :
        self.__index = index
        return index

    def __eq__(self, other) :
        if isinstance(other, Vertex) :
            return (self is other) or (self.__data == other.__data and
                                       self.__index == other.__index)
        elif isinstance(self.__index, type(other)) or \
             isinstance(other, type(self.__index)) :
            return self.__index == other
        else :
            return False

    def copy(self) :
        if Copyable.iscopyable(self.__data):
            out = Vertex(self.__data.copy(), self.getindex())
            return out
        else :
            return Vertex(self.__data, self.getindex())

    def __str__(self) :
        if self.getdata() is not None :
            return f"({self.getindex()}: {self.getdata()})"
        else :
            return f"({self.getindex()})"
    
    def __hash__(self) :
        return self.getindex()

class Edge(Copyable) :
    def __init__(self, index, start, end, length = 1) :
        self.__start = start
        self.__end = end
        self.__length = length
        self.__index = index

    def getstart(self) :
        return self.__start

    def getend(self) :
        return self.__end

    def getlength(self) :
        return self.__length

    def setstart(self, vert) :
        self.__start = vert
        return vert

    def setend(self, vert) :
        self.__end = vert
        return vert

    def setlength(self, length) :
        self.__length = length
        return length

    def getindex(self) :
        return self.__index

    def _setindex(self, index) :
        self.__index = index
        return self.__index

    def cantraverse(self, vert) :
        return (self.getstart() == vert)

    def traverse(self, vert) :
        assert(self.getstart() == vert)
        return (self.getend(), self.getlength())

    def __eq__(self, other) :
        if isinstance(other, Edge) :
            return (self is other) or (self.__length == other.__length and
                                       self.__start == other.__start and
                                       self.__end == other.__end)
        elif isinstance(self.__index, type(other)) or \
             isinstance(other, type(self.__index)) :
            return self.getindex() == other
        else :
            return False

    def copy(self) :
        if Copyable.iscopyable(self.__length) :
            return Edge(self.getindex(), self.__start.copy(),
                        self.__end.copy(), self.__length.copy())
        else :
            return Edge(self.getindex(), self.__start.copy(),
                        self.__end.copy(), self.__length)
    def __str__(self) :
        if self.getlength() is not None :
            return f"[{self.getindex()} : " + \
                   f"{self.getstart()} -> {self.getend()} ({self.getlength()})]"
        else :
            return f"[{self.getindex()} : " +\
                   f"{self.getstart()} -> {self.getend()}]"
    
    def __hash__(self) :
        return self.getindex()
        

class UndirectedEdge(Edge) :
    """
Undirected edges.
"""
    def __init__(self, index, start, end, length = 1) :
        super().__init__(index, start, end, length)

    def cantraverse(self, vert) :
        return (self.getstart() == vert or self.getend() == vert)

    def traverse(self, vert) :
        if self.getstart() == vert :
            return (self.getend(), self.getlength())
        elif self.getend() == vert :
            return (self.getstart(), self.getlength())
        else :
            raise Exception("Vertex not the start or end of the edge.")
    def copy(self) :
        if Copyable.iscopyable(self.getlength()) :
            return UndirectedEdge(self.getindex(), self.getstart().copy(),
                                  self.getend().copy(), self.getlength().copy())
        else :
            return UndirectedEdge(self.getindex(), self.getstart().copy(),
                                     self.getend().copy(), self.getlength())
    def __eq__(self, other) :
        if isinstance(other, UndirectedEdge) :
            return (self is other) or (self.getlength() == other.getlength() and
                                       (self.getstart() == other.getstart() and
                                       self.getend() == other.getend()) or
                                       (self.getstart() == other.getend() and
                                        self.getend() == other.getstart()))
        elif isinstance(self.getindex(), type(other)) or \
             isinstance(other, type(self.getindex())) :
            return self.getindex() == other
        else :
            return False

    def __str__(self) :
        if self.getlength() is not None :
            return f"[{self.getindex()} : " + \
                   f"{self.getstart()} <-> {self.getend()} ({self.getlength()})]"
        else :
            return f"[{self.getindex()} : " + \
                   f"{self.getstart()} <-> {self.getend()}]"

class VertexFactory(despats.Singleton) :
    def __init__(self) :
        self.__index = 0

    def makevertex(self, data = None) :
        out = Vertex(data, self.__index)
        self.__index += 1
        return out
    def makevertex_list(self, nverts : int, data = None) :
        if hasattr(data, "__iter__") :
            return [VertexFactory.getsingleton().makevertex(d)
                    for d, _ in zip(data, range(nverts))]
        else :
            return [VertexFactory.getsingleton().makevertex(data)
                    for _ in range(nverts)]

class EdgeFactory(despats.Singleton) :
    def __init__(self) :
        self.__index = 0

    def makeedge(self, start, end, length = 1, directed = True) :
        if directed :
            out = Edge(self.__index, start, end, length)
            self.__index += 1
            return out
        else :
            out = UndirectedEdge(self.__index, start, end, length)
            self.__index += 1
            return out
    
# Base representation.
class Graph(Copyable) :
    """
Represents a general graph.
"""

    def __init__(self, verts, edges) :
        if verts == None :
            self.__verts = list()
        else :
            self.__verts = verts
        if edges == None :
            self.__edges = list()
        else :
            self.__edges = edges

    def getverts(self) :
        return self.__verts

    def getvert(self, index) :
        for v in self.getverts() :
            if v.getindex() == index or v == index:
                return v
        return None

    def getedges(self) :
        return self.__edges

    def getedge(self, index, cutoff = 1e-6) :
        if hasattr(index, "__iter__") :
            for e in self.getedges() :
                if isinstance(e, UndirectedEdge) :
                    if ((e.getstart() == index[0] and e.getend() == index[1]) or\
                       (e.getstart() == index[1] and e.getend() == index[0])) \
                        and ((len(index) == 3 and \
                              abs(e.getlength() - index[2]) < cutoff) or
                             len(index) != 3) :
                        return e
                else :
                    if (e.getstart() == index[0] and e.getend() == index[1]) and \
                       ((len(index) == 3 and \
                         abs(e.getlengt() - index[2]) < cutoff) or
                        len(index) != 3) :
                        return e
        else :
            for e in self.getedges() :
                if e.getindex() == index :
                    return e
        return None

    def addverts(self, vert) :
        """
Can do single vertices or a collection of vertices.
"""
        if hasattr(vert, "__iter__") :
            assert(all(map(lambda x : isinstance(x, Vertex), vert)))
            for v in vert :
                self.__verts.append(v)
        else :
            self.__verts.append(vert)
        return self.__verts
    
    def addedges(self, edge) :
        """
Can do singe edges or a collection of edges.
"""
        if hasattr(edge, "__iter__") :
            assert(all(map(lambda x : isinstance(x, Edge), edge)))
            for e in edge :
                self.__edges.append(e)
        elif isinstance(edge, Edge) :
            self.__edges.append(edge)
        return self.__edges
            
    def hasvertex(self, vert) :
        return vert in self.getverts()

    def hasedge(self, edge) :
        return edge in self.getedges()

    def getneighbors(self, vert) :
        neigh = []
        for e in self.getedges() :
            if e.cantraverse(vert) :
                neigh.append(tuple(list(e.traverse(vert)) + [
                                   isinstance(e, UndirectedEdge)]))
        return neigh

    def __str__(self) :
        return "{" + str(self.getedges()) + ", " + str(self.getverts()) + "}"
    
def dijkstra(graph : Graph, start : Vertex, end : Vertex) :
    visited = {start : (0, None)}
    openset = [(start, n) for n in graph.getneighbors(start)]

    while len(openset) > 0:
        vert = openset.pop()
        dist = visited[vert[0]][0] + vert[1][1]
        if (vert[1][0] in visited.keys() and visited[vert[1][0]][0] > dist) or \
           vert[1][0] not in visited.keys() :
            # Update if vertex is new, or if the distance it has is shorter.
            visited[vert[1][0]] = (dist, vert[0])
            # Only generate neighbors if it was added.
            openset = openset + [(vert[1][0], n) for n in
                                 graph.getneighbors(vert[1][0])]
    if end in visited.keys() :
        verts = []
        edges = []
        curr = end
        while curr != start :
            verts.append(curr)
            edges.append(graph.getedge((visited[curr][1], curr,
                                     visited[curr][0] -
                                     visited[visited[curr][1]][0])))
            curr = visited[curr][1]
            
        print(Graph(verts, edges))
        return Graph(verts, edges)
    else :
        return None
