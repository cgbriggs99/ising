#!/usr/bin/python3


import pytest
import ising

nverts = 4
# Königsberg, prewar
old_k = [(0, 1, 200), (0, 1, 200), (0, 2, 135), (0, 3, 102), (0, 3, 126),
             (2, 3, 237), (1, 2, 225)]
# Kaliningrad, postwar
new_k = [(0, 1, 200), (0, 2, 135), (0, 3, 102), (1, 2, 225), (1, 2, 238),
         (1, 3, 325), (2, 3, 237), (2, 3, 177), (2, 3, 320)]

def test_graph() :
    verts1 = ising.graph.VertexFactory.getsingleton().makevertex_list(nverts)
    verts2 = ising.graph.VertexFactory.getsingleton().makevertex_list(nverts)
    konig = ising.graph.Graph([], [])
    kalin = ising.graph.Graph([], [])

    konig.addverts(verts1[0])
    konig.addverts(verts1[1:])
    kalin.addverts(verts2)

    for e in old_k :
        konig.addedges(ising.graph.EdgeFactory.getsingleton().makeedge(
            verts1[e[0]], verts1[e[1]], e[2], directed = False))
    kalin.addedges([ising.graph.EdgeFactory.getsingleton().makeedge(
            verts2[e[0]], verts2[e[1]], e[2], directed = False) for e in new_k])
    assert(verts1[0].getdata() is None)
    verts1[0].setdata("Test")
    assert(verts1[0].getdata() == "Test")
    assert(verts1[0].getindex() < verts2[0].getindex())
    assert(verts1[0] == verts1[0])
    assert(verts1[0] != verts1[1])
    assert(str(verts1[0]) is not None)
    assert(konig.getedges()[0].getstart() == verts1[0])
    assert(konig.getedges()[0].getend() == verts1[1])
    assert(konig.getedges()[0].getlength() == old_k[0][2])
    assert(konig.getedges()[0].setstart(verts1[1]) == verts1[1])
    assert(konig.getedges()[0].setend(verts1[0]) == verts1[0])
    assert(konig.getedges()[0].setlen(150) == 150)
    assert(konig.getedges()[0].getindex() >= 0)
    assert(konig.getedges()[0].traverse(verts1[1])[0] == verts1[0])
    assert(konig.getedges()[1] == konig.getedges()[1])
    assert(konig.getedges()[0].copy() is not None)
    assert(str(konig.getedges()[0]) is not None)
    assert(konig.getverts() is not None)
    assert(konig.getvert(verts1[0].getindex()) is not None)
    assert(konig.getedges() is not None)
    assert(konig.getedge((0, 1, 200)) is not None)
    assert(konig.getedge(konig.getedges()[0]) is not None)
    assert(konig.hasvertex(verts1[0]))
    assert(konig.hasedge(konig.getedges()[0]))
    assert(konig.getneighbors(verts1[0]) is not None)
    assert(str(konig) is not None)
    assert(ising.graph.dijkstra(konig, verts1[1], verts1[3]) is not None)
    
    
