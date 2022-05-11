#!/usr/bin/python3

"""
Test the thermodynamic calculations.
"""


import math
import numpy as np
import pytest
import ising

__LENGTH = 10
__J = -2
__M = 1.1
__K = 1
__TEMP = 298.15


def test_thermo():
    """
Test the partition, average, and variance.
"""
    # Set up the hamiltonian.
    ham = ising.hamiltonian.PeriodicHamiltonian(__J, __M)
    # Set the strategy.
    ising.thermo.ThermoMethod.getsingleton().setstrat(
        ising.thermo.FullCalcStrategy.getsingleton()
    )

    part = ising.thermo.ThermoMethod.getsingleton().partition(
        ham, __LENGTH, __TEMP, __K
    )
    # Make sure nothing blows up
    assert math.isfinite(part) and part > 0
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
    assert math.isfinite(variance) and math.log10(abs(variance)) < 12


def test_plots():
    """
Test energy, heat capacity, and magnetic susceptibility.
"""
    plots = ising.thermo.PlotValsMethod.getsingleton()
    plots.setstrat(ising.thermo.SequentialStrategy.getsingleton())
    ham = ising.hamiltonian.PeriodicHamiltonian(__J, __M)
    points = list(np.linspace(0.1, 20))
    assert isinstance(plots.getstrat(), ising.thermo.SequentialStrategy)
    seq_e, seq_h, seq_m = plots.calc_plot_vals(ham, __LENGTH, points, __K)
    plots.setstrat(ising.thermo.ThreadedStrategy.getsingleton())
    thr_e, thr_h, thr_m = plots.calc_plot_vals(ham, __LENGTH, points, __K)
    plots.setstrat(ising.fastcwrapper.CPlotStrategy.getsingleton())
    cpl_e, cpl_h, cpl_m = plots.calc_plot_vals(ham, __LENGTH, points, __K)
    assert all(
        map(
            lambda s, t, c: abs(s - c) <= 1e-4 and abs(t - c) <= 1e-4,
            seq_e,
            thr_e,
            cpl_e,
        )
    )
    assert all(
        map(
            lambda s, t, c: abs(s - c) <= 1e-4 and abs(t - c) <= 1e-4,
            seq_h,
            thr_h,
            cpl_h,
        )
    )
    assert all(
        map(
            lambda s, t, c: abs(s - c) <= 1e-4 and abs(t - c) <= 1e-4,
            seq_m,
            thr_m,
            cpl_m,
        )
    )
