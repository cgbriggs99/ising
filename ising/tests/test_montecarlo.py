import pytest
import ising
import math

__length = 10
__J = -2
__M = 1.1
__k = 1
__temp = 0.1

def test_montecarlo() :
    # Set up the hamiltonian.
    ham = ising.PeriodicHamiltonian(__J, __M)
    # Set the strategy.
    ising.thermo.ThermoMethod.getsingleton().setstrat(
        ising.montecarlo.MonteCarloStrategy.getsingleton())
    ising.montecarlo.MonteCarloStrategy.getsingleton().setpoints(100)
    assert(ising.montecarlo.MonteCarloStrategy.getsingleton().getpoints() == 100)
    
    
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
    assert(math.isfinite(variance) and variance >= 0 and (variance == 0 or math.log10(abs(variance)) < 12))

def test_metropolis() :
    # Set up the hamiltonian.
    ham = ising.PeriodicHamiltonian(__J, __M)
    # Set the strategy.
    ising.thermo.ThermoMethod.getsingleton().setstrat(
        ising.montecarlo.MetropolisStrategy.getsingleton())
    ising.montecarlo.MetropolisStrategy.getsingleton().setpoints(100)
    assert(ising.montecarlo.MetropolisStrategy.getsingleton().getpoints() == 100)

    ising.montecarlo.MetropolisStrategy.getsingleton().setdepth(20)
    assert(ising.montecarlo.MetropolisStrategy.getsingleton().getdepth() == 20)
    
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
