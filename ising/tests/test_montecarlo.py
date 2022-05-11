"""
Tests the Monte-Carlo and Metropolis sampling.
"""

import math
import pytest
import ising

__LENGTH = 10
__J = -2
__M = 1.1
__K = 1
__TEMP = 0.1


def test_montecarlo():
    """
Test the naive Monte-Carlo.
"""
    # Set up the hamiltonian.
    ham = ising.PeriodicHamiltonian(__J, __M)
    # Set the strategy.
    ising.thermo.ThermoMethod.getsingleton().setstrat(
        ising.montecarlo.MonteCarloStrategy.getsingleton()
    )
    ising.montecarlo.MonteCarloStrategy.getsingleton().setpoints(100)
    assert ising.montecarlo.MonteCarloStrategy.getsingleton().getpoints() == 100

    energy = ising.thermo.ThermoMethod.getsingleton().average(
        ham.energy, ham, __LENGTH, temp=__TEMP, boltzmann=__K
    )
    assert (
        math.isfinite(energy)
        and math.log10(abs(energy)) < 12
        and math.log10(abs(energy)) > -12
    )
    variance = ising.thermo.ThermoMethod.getsingleton().variance(
        ham.energy, ham, __LENGTH, temp=__TEMP, boltzmann=__K
    )
    assert (
        math.isfinite(variance)
        and variance >= 0
        and (variance == 0 or math.log10(abs(variance)) < 12)
    )


def test_metropolis():
    """
Tests the Metropolis sampling.
"""
    # Set up the hamiltonian.
    ham = ising.PeriodicHamiltonian(__J, __M)
    # Set the strategy.
    ising.thermo.ThermoMethod.getsingleton().setstrat(
        ising.montecarlo.MetropolisStrategy.getsingleton()
    )
    ising.montecarlo.MetropolisStrategy.getsingleton().setpoints(100)
    assert ising.montecarlo.MetropolisStrategy.getsingleton().getpoints() == 100

    ising.montecarlo.MetropolisStrategy.getsingleton().setdepth(20)
    assert ising.montecarlo.MetropolisStrategy.getsingleton().getdepth() == 20

    energy = ising.thermo.ThermoMethod.getsingleton().average(
        ham.energy, ham, __LENGTH, temp=__TEMP, boltzmann=__K
    )
    assert (
        math.isfinite(energy)
        and math.log10(abs(energy)) < 12
        and math.log10(abs(energy)) > -12
    )
    variance = ising.thermo.ThermoMethod.getsingleton().variance(
        ham.energy, ham, __LENGTH, temp=__TEMP, boltzmann=__K
    )
    assert (
        math.isfinite(variance)
        and variance >= 0
        and (variance == 0 or math.log10(abs(variance)) < 12)
    )
