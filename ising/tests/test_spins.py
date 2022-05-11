#!/usr/bin/python3

"""
Test spin configurations.
"""

import random
import pytest
import ising

__MATRIX = [1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1]
__VALUE = 0b11010001001
__LENGTH = len(__MATRIX)
__TRIES = 3


def test_spinmatrix():
    """
Test matrix spin configuration.
"""
    spin = ising.SpinMatrix(__MATRIX)
    assert len(spin) == len(__MATRIX)
    assert spin.magnetization() == -1
    # Test getitem
    for _ in range(__TRIES):
        ind = random.randint(0, len(spin) - 1)
        assert spin[ind] == __MATRIX[ind]
    # Test iter
    for i, j in zip(spin, __MATRIX):
        assert i == j
    ind = random.randint(0, len(spin) - 1)
    spin[ind] = -spin[ind]
    assert spin[ind] != __MATRIX[ind]
    assert len(str(spin)) == len(spin)
    assert spin[-1] == spin[len(spin) - 1]
    assert spin[len(spin)] == spin[0]


def test_spinint():
    """
Test integer spin configuration.
"""
    spin = ising.SpinInteger(__VALUE, __LENGTH)
    assert len(spin) == __LENGTH
    assert spin.magnetization() == -1
    # Test getitem
    for i in range(__TRIES):
        ind = random.randint(0, len(spin) - 1)
        assert spin[ind] == __MATRIX[ind]
    # Test iter
    assert iter(spin) is not spin
    itr = iter(spin)
    assert iter(itr) is itr
    for i, j in zip(spin, __MATRIX):
        assert i == j
    ind = random.randint(0, len(spin) - 1)
    spin[ind] = -spin[ind]
    assert spin[ind] != __MATRIX[ind]
    assert len(str(spin)) == len(spin)
    assert spin[-1] == spin[len(spin) - 1]
    assert spin[len(spin)] == spin[0]
