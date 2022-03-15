#!/usr/bin/python3

import pytest
import ising
import math
import numpy as np

__length = 10
__J = -2
__M = 1.1
__k = 1
__temps = np.linspace(1, 100, 50)
__threads = 4

def test_fafb() :
    # Test the backend.
    e, h, m = ising.src.fafb.plot_vals(__length, __J, __M, list(__temps), __k,
                                       __threads)
    assert(any(map(lambda x: x != 0, e + h + m)))
