#!/usr/bin/python3

import pytest
import ising
import math

__length = 10
__J = -2
__M = 1.1
__k = 1
__temp = 0.1

def test_thermo() :
    ham = ising.Hamiltonian(__J, __M)
    part = ising.partition(ham, __length, __temp, __k)
    assert(math.isfinite(part) and part > 0)
    energy = ising.average_value(ham.energy, ham, __length, __temp, __k)
    assert(math.isfinite(energy) and math.log10(abs(energy)) < 12 and
           math.log10(abs(energy)) > -12)
    variance = ising.variance(ham.energy, ham, __length, __temp, __k)
    assert(math.isfinite(variance) and math.log10(abs(variance)) < 12)
