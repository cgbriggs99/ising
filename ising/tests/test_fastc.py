#!/usr/bin/python3

import pytest
import ising
import math
import numpy as np
import os
import time

__length = 8
__J = -2
__M = 1.1
__k = 1
__temps = np.linspace(1, 100, 50)
__threads = 4

def test_fastc() :
    # Test the backend.
    ham = ising.PeriodicHamiltonian(__J, __M)
    t1 = time.perf_counter()
    e, h, m = ising.fastcwrapper.plotvals(ham, __length, __temps, __k,
                                       __threads, no_c = True)
    t2 = time.perf_counter()
    assert(any(map(lambda x: x != 0, e + h + m)))
    t3 = time.perf_counter()
    e, h, m = ising.fastcwrapper.plotvals(ham, __length, __temps, __k,
                                       __threads)
    t4 = time.perf_counter()
    assert(any(map(lambda x: x != 0, e + h + m)))

    assert(abs((t4 - t3) / (t2 - t1)) < 0.1)
