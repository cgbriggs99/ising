#!/usr/bin/python3

"""
Test the Hamiltonians.
"""

import pytest
import ising


__MATRIX = [1, 1, 1, 1]
__J = -2
__M = 1.1
__CONNS = [(0, 1, __J), (1, 2, __J), (2, 3, __J), (3, 0, __J)]
__MAGS = [1.1, 1.1, 1.1, 1.1]


def test_perhamiltonian():
    """
Test periodic Hamiltonians.
"""
    # Set up a hamiltonian.
    ham = ising.PeriodicHamiltonian(1, 2)
    # Make sure storage works.
    assert ham.getcoupling() == 1
    assert ham.getmagnet() == 2
    ham.setcoupling(__J)
    ham.setmagnet(__M)
    assert ham.getcoupling() == __J
    assert ham.getmagnet() == __M
    # Do a sample calculation.
    assert ham.energy(ising.SpinMatrix(__MATRIX)) == 4 * -__J + __M * 4
    assert ham.temperature(ising.SpinMatrix(__MATRIX), 1) == 4 * -__J + __M * 4


def test_nonperhamiltonian():
    """
Test non-periodic Hamiltonians.
"""
    # Set up a hamiltonian.
    ham = ising.NPHamiltonian(1, 2)
    # Make sure storage works.
    assert ham.getcoupling() == 1
    assert ham.getmagnet() == 2
    ham.setcoupling(__J)
    ham.setmagnet(__M)
    assert ham.getcoupling() == __J
    assert ham.getmagnet() == __M
    # Do a sample calculation.
    assert ham.energy(ising.SpinMatrix(__MATRIX)) == 3 * -__J + __M * 4
    assert ham.temperature(ising.SpinMatrix(__MATRIX), 1) == 3 * -__J + __M * 4


def test_graphhamiltonian():
    """
Test general graph Hamiltonians.
"""
    # Set up a hamiltonian.
    verts = [
        ising.graph.VertexFactory.getsingleton().makevertex(i)
        for i in range(len(__MATRIX))
    ]
    graph = ising.graph.Graph(verts, [])
    graph.addedges(
        [
            ising.graph.EdgeFactory.getsingleton().makeedge(
                graph.getvert(verts[edg[0]]),
                graph.getvert(verts[edg[1]]),
                edg[2],
                directed=False,
            )
            for edg in __CONNS
        ]
    )
    ham = ising.hamiltonian.GraphHamiltonian(graph, 2)
    # Make sure storage works.
    assert ham.getmagnet() == 2
    ham.setmagnet(__M)
    assert ham.getmagnet() == __M
    # Do a sample calculation.
    assert ham.energy(ising.SpinMatrix(__MATRIX)) == 4 * -__J + __M * 4
    assert ham.temperature(ising.SpinMatrix(__MATRIX), 1) == 4 * -__J + __M * 4
    ham.setmagnet(__MAGS)
    assert ham.energy(ising.SpinMatrix(__MATRIX)) == 4 * -__J + __M * 4
    assert ham.temperature(ising.SpinMatrix(__MATRIX), 1) == 4 * -__J + __M * 4
