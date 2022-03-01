#!/usr/bin/python3

import pytest
import ising
import random

__matrix = [1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1]
__value = 0b11010001001
__length = 11
__tries = 3

def test_spinmatrix() :
    sc = ising.SpinMatrix(__matrix)
    assert(len(sc) == len(__matrix))
    # Test getitem
    for i in range(__tries) :
        ind = random.randint(0, len(sc) - 1)
        assert(sc[ind] == __matrix[ind])
    # Test iter
    for i, j in zip(sc, __matrix) :
        assert(i == j)
    ind = random.randint(0, len(sc) - 1)
    sc[ind] = -sc[ind]
    assert(sc[ind] != __matrix[ind])
    assert(sc.magnetization() == -1)

def test_spinint() :
    sc = ising.SpinInteger(__value, __length)
    assert(len(sc) == __length)
    # Test getitem
    for i in range(__tries) :
        ind = random.randint(0, len(sc) - 1)
        assert(sc[ind] == __matrix[ind])
    # Test iter
    assert(iter(sc) is not sc)
    for i, j in zip(sc, __matrix) :
        assert(i == j)
    ind = random.randint(0, len(sc) - 1)
    sc[ind] = -sc[ind]
    assert(sc[ind] != __matrix[ind])
    assert(sc.magnetization() == -1)


    
