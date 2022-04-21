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
    # Set up the hamiltonian.
    ham = ising.PeriodicHamiltonian(__J, __M)
    # Set the strategy.
    ising.thermo.ThermoMethod.getsingleton().setstrat(
        ising.thermo.FullCalcStrategy.getsingleton())
    
    part = ising.thermo.ThermoMethod.getsingleton().partition(
        ham, __length, __temp, __k)
    # Make sure nothing blows up
    assert(math.isfinite(part) and part > 0)
    energy = ising.thermo.ThermoMethod.getsingleton().average(
        ham.energy, ham, __length, __temp, __k)
    assert(math.isfinite(energy) and math.log10(abs(energy)) < 12 and
           math.log10(abs(energy)) > -12)
    variance = ising.thermo.ThermoMethod.getsingleton().variance(
        ham.energy, ham, __length, __temp, __k)
    assert(math.isfinite(variance) and math.log10(abs(variance)) < 12)
