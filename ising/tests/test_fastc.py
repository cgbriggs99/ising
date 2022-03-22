#!/usr/bin/python3

import pytest
import ising
import math
import numpy as np
import os

__length = 10
__J = -2
__M = 1.1
__k = 1
__temps = np.linspace(1, 100, 50)
__threads = 4

def test_fastc() :
    # Test the backend.
    ham = ising.Hamiltonian(__J, __M)
    e, h, m = ising.fastcwrapper(ham, __length, __temps, __k,
                                       __threads, no_c = True)
    assert(any(map(lambda x: x != 0, e + h + m)))
    e, h, m = ising.fastcwrapper(ham, __length, __temps, __k,
                                       __threads)
    assert(any(map(lambda x: x != 0, e + h + m)))
