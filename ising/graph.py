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

    def _setindex(self, index) :
        self.__index = index
        return index

    def __eq__(self, other) :
        if isinstance(other, Vertex) :
            return (self is other) or (self.__data == other.__data and \
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
            return Vertex(data, self.getindex())

    def __str__(self) :
        if self.getdata() is not None :
            return f"({self.getindex()}: {self.getdata()})"
        else :
            return f"({self.getindex()})"
        

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

    def setlen(self, length) :
        self.__length = length
        return length

    def getindex(self) :
        return self.__index

    def _setindex(self, index) :
        self.__index = index
        return self.__index

    def traverse(self, vert) :
        assert(self.__start == vert)
        return (self.__end, self.__length)

    def __eq__(self, other) :
        if isinstance(other, Edge) :
            return (self is other) or (self.__length == other.__length and \
                   self.__index == other.__index and
                                       self.__start == other.__start and
                                       self.__end == other.__end)
        elif isinstance(self.__index, type(other)) or \
             isinstance(other, type(self.__index)) :
            return self.__index == other
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
        

class UndirectedEdge(Edge) :
    """
Undirected edges.
"""
    def __init__(self, index, start, end, length = 1) :
        super(Edge).__init__(index, start, end, length)

    def traverse(self, vert) :
        if self.__start == vert :
            return (self.__end, self.__length)
        elif self.__end = vert :
            return (self.__start, self.__length)
        else :
            raise Exception("Vertex not the start or end of the edge.")
    def copy(self) :
        if Copyable.iscopyable(self.__length) :
            return UndirectedEdge(self.getindex(), self.getstart().copy(),
                                  self.getend().copy(), self.getlength().copy())
        else :
            return UndirectedEdge(self.getindex(), self.getstart().copy(),
                                  self.getend().copy(), self.getlength())

    def __str__(self) :
        if self.getlength() is not None :
            return f"[{self.getindex()} : " + \
                   f"{self.getstart()} <-> {self.getend()} ({self.getlength()})]"
        else :
            return f"[{self.getindex()} : " +\
                   f"{self.getstart()} <-> {self.getend()}]"

class VertexFactory(despats.Singleton) :
    def __init__(self) :
        self.__index = 0

    def makevertex(self, data = None) :
        out = Vertex(data, self.__index)
        self.__index += 1
        return out

class EdgeFactory(despats.Singleton) :
    def __init__(self) :
        self.__index = 0

    def makeedge(self, *args, **kwargs) :
        if "directed" in kwargs and kwargs["directed"] == True :
            out = UndirectedEdge(self.__index, *args)
            self.__index += 1
            return out
        else :
            out = Edge(self.__index, *args)
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
        else
            self.__verts = verts
        if edges == None :
            self.__edges = list()
        else :
            self.__edges = edges

    def getverts(self) :
        return self.__verts

    def getedges(self) :
        return self.__edges

    def addverts(self, vert) :
        """
Can do single vertices or a collection of vertices.
"""
        if hasattr(vert, "__iter__") :
            for v in vert :
                self.__verts.add(v)
        else :
            self.__verts.add(vert)
        return self.__verts
    
    def addedges(self, edge) :
        """
Can do singe edges or a collection of edges.
"""
        if hasattr(edge, "__iter__") :
            assert(all(map(lambda x : isinstance(x, Edge), edge)))
            for e in edge :
                self.__edges.add(e)
        elif isinstance(edge, Edge) :
            self.__edges.add(edge)
        return self.__edges
            
    def hasvertex(self, vert) :
        return vert in self.getverts()

    def hasedge(self, edge) :
        return edge in self.getedges()

    def getneighbors(self, vert) :
        neigh = []
        for e in self.getedges() :
            try :
                neigh.add(tuple(e.traverse(vert)))
            except :
                pass
        return neigh

    def __str__(self) :
        return "{" + str(self.getedges()) + ", " + str(self.getverts()) + "}"
    
    
    
