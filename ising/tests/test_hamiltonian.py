#!/usr/bin/python3

import pytest
import ising
import random


__matrix = [1, 1, 1, 1]
__J = -2
__M = 1.1

def test_hamiltonian() :
    # Set up a hamiltonian.
    ham = ising.Hamiltonian(1, 2)
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
    
