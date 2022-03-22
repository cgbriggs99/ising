#!/usr/bin/python3

import pytest
import ising
import random

__matrix = [1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1]
__value = 0b11010001001
__length = len(__matrix)
__tries = 3

def test_spinmatrix() :
    sc = ising.SpinMatrix(__matrix)
    assert(len(sc) == len(__matrix))
    assert(sc.magnetization() == -1)
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
    assert(len(str(sc)) == len(sc))
    assert(sc[-1] == sc[len(sc) - 1])
    assert(sc[len(sc)] == sc[0])

def test_spinint() :
    sc = ising.SpinInteger(__value, __length)
    assert(len(sc) == __length)
    assert(sc.magnetization() == -1)
    # Test getitem
    for i in range(__tries) :
        ind = random.randint(0, len(sc) - 1)
        assert(sc[ind] == __matrix[ind])
    # Test iter
    assert(iter(sc) is not sc)
    it = iter(sc)
    assert(iter(it) is it)
    for i, j in zip(sc, __matrix) :
        assert(i == j)
    ind = random.randint(0, len(sc) - 1)
    sc[ind] = -sc[ind]
    assert(sc[ind] != __matrix[ind])
    assert(len(str(sc)) == len(sc))
    assert(sc[-1] == sc[len(sc) - 1])
    assert(sc[len(sc)] == sc[0])


    
