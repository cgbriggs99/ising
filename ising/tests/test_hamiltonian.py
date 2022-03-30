#!/usr/bin/python3

import pytest
import ising
import random


__matrix = [1, 1, 1, 1]
__J = -2
__M = 1.1
__conns = [(0, 1, __J), (1, 2, __J), (2, 3, __J), (3, 0, __J)]
__mags = [1.1, 1.1, 1.1, 1.1]


def test_perhamiltonian() :
    # Set up a hamiltonian.
    ham = ising.PeriodicHamiltonian(1, 2)
    # Make sure storage works.
    assert(ham.getcoupling() == 1)
    assert(ham.getmagnet() == 2)
    ham.setcoupling(__J)
    ham.setmagnet(__M)
    assert(ham.getcoupling() == __J)
    assert(ham.getmagnet() == __M)
    # Do a sample calculation.
    assert(ham.energy(ising.SpinMatrix(__matrix)) == 4 * -__J + __M * 4)
    assert(ham.temperature(ising.SpinMatrix(__matrix), 1) == 4 * -__J +\
           __M * 4)
    
def test_nonperhamiltonian() :
    # Set up a hamiltonian.
    ham = ising.NPHamiltonian(1, 2)
    # Make sure storage works.
    assert(ham.getcoupling() == 1)
    assert(ham.getmagnet() == 2)
    ham.setcoupling(__J)
    ham.setmagnet(__M)
    assert(ham.getcoupling() == __J)
    assert(ham.getmagnet() == __M)
    # Do a sample calculation.
    assert(ham.energy(ising.SpinMatrix(__matrix)) == 3 * -__J + __M * 4)
    assert(ham.temperature(ising.SpinMatrix(__matrix), 1) == 3 * -__J +\
           __M * 4)

def test_graphhamiltonian() :
    # Set up a hamiltonian.
    verts = [ising.graph.VertexFactory.getsingleton().makevertex(i)
             for i in range(len(__matrix))]
    graph = ising.graph.Graph(verts, [])
    graph.addedges([ising.graph.EdgeFactory.getsingleton().makeedge(
        graph.getvert(verts[e[0]]), graph.getvert(verts[e[1]]), e[2],
        directed = False)
                    for e in __conns])
    ham = ising.hamiltonian.GraphHamiltonian(graph, 2)
    # Make sure storage works.
    assert(ham.getmagnet() == 2)
    ham.setmagnet(__M)
    assert(ham.getmagnet() == __M)
    # Do a sample calculation.
    assert(ham.energy(ising.SpinMatrix(__matrix)) == 4 * -__J + __M * 4)
    assert(ham.temperature(ising.SpinMatrix(__matrix), 1) == 4 * -__J +\
           __M * 4)
    ham.setmagnet(__mags)
    assert(ham.energy(ising.SpinMatrix(__matrix)) == 4 * -__J + __M * 4)
    assert(ham.temperature(ising.SpinMatrix(__matrix), 1) == 4 * -__J +\
           __M * 4)
