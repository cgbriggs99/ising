#!/usr/bin/python3

"""
Tests the C backend.
"""

import time
import random
import pytest
import ising

__LENGTH = 8
__J = -2
__M = 1.1
__K = 1
__THREADS = 4


def test_fastc():
    """
Test the C backend.
"""
    ham = ising.PeriodicHamiltonian(__J, __M)
    thermo = ising.thermo.ThermoMethod.getsingleton()
    thermo.setstrat(ising.fastcwrapper.CThermoStrategy.getsingleton())
    ising.fastcwrapper.CThermoStrategy.getsingleton().setthreads(__THREADS)
    for _ in range(100):
        spin = random.randrange(256)
        assert ham.energy(
            ising.spins.SpinInteger(spin, __LENGTH)
        ) == ising.fastc.energy(spin, __LENGTH, __J, __M)
        assert ising.spins.SpinInteger(
            spin, __LENGTH
        ).magnetization() == ising.fastc.magnet(spin, __LENGTH)
    time1 = time.perf_counter()
    part1 = thermo.partition(ham, __LENGTH, boltzmann=__K)
    avg1 = thermo.average(ham.energy, ham, __LENGTH, boltzmann=__K)
    var1 = thermo.variance(ham.energy, ham, __LENGTH, boltzmann=__K)
    time2 = time.perf_counter()
    thermo.setstrat(ising.thermo.FullCalcStrategy.getsingleton())
    time3 = time.perf_counter()
    part2 = thermo.partition(ham, __LENGTH, boltzmann=__K)
    avg2 = thermo.average(ham.energy, ham, __LENGTH, boltzmann=__K)
    var2 = thermo.variance(ham.energy, ham, __LENGTH, boltzmann=__K)
    time4 = time.perf_counter()

    assert abs(part1 - part2) < 1e-4
    assert abs(avg1 - avg2) < 1e-4
    assert abs(var1 - var2) < 1e-4
    assert abs(time2 - time1) < abs(time4 - time3) / 2
