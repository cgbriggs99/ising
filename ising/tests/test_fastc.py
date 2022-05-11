#!/usr/bin/python3

import pytest
import ising
import math
import numpy as np
import os
import time
import random

__length = 8
__J = -2
__M = 1.1
__k = 1
__threads = 4

def test_fastc() :
    # Test the backend.
    ham = ising.PeriodicHamiltonian(__J, __M)
    thermo = ising.thermo.ThermoMethod.getsingleton()
    thermo.setstrat(ising.fastcwrapper.CThermoStrategy.getsingleton())
    ising.fastcwrapper.CThermoStrategy.getsingleton().setthreads(2)
    for i in range(100) :
        sp = random.randrange(256)
        assert(ham.energy(ising.spins.SpinInteger(sp, __length)) == ising.fastc.energy(sp,
                                                                             __length,
                                                                             __J, __M))
        assert(ising.spins.SpinInteger(sp, __length).magnetization() ==
               ising.fastc.magnet(sp, __length))
    t1 = time.perf_counter()
    p1 = thermo.partition(ham, __length, boltzmann = 1)
    a1 = thermo.average(lambda sp: ham.energy(sp), ham, __length, boltzmann = 1)
    v1 = thermo.variance(ham.energy, ham, __length, boltzmann = 1)
    t2 = time.perf_counter()
    thermo.setstrat(ising.thermo.FullCalcStrategy.getsingleton())
    t3 = time.perf_counter()
    p2 = thermo.partition(ham, __length, boltzmann = 1)
    a2 = thermo.average(ham.energy, ham, __length, boltzmann = 1)
    v2 = thermo.variance(ham.energy, ham, __length, boltzmann = 1)
    t4 = time.perf_counter()

    assert(abs(p1 - p2) < 1e-4)
    assert(abs(a1 - a2) < 1e-4)
    assert(abs(v1 - v2) < 1e-4)
    assert(abs(t2 - t1) < abs(t4 - t3) / 2)
