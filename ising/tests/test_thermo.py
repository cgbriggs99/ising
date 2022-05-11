#!/usr/bin/python3

import pytest
import ising
import math
import numpy as np

__length = 8
__J = -2
__M = 1.1
__k = 1
__temp = 298.15

def test_thermo() :
    # Set up the hamiltonian.
    ham = ising.hamiltonian.PeriodicHamiltonian(__J, __M)
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
    ising.thermo.ThermoMethod.getsingleton().setstrat(ising.fastcwrapper.CThermoStrategy.getsingleton())
    assert(math.isfinite(variance) and math.log10(abs(variance)) < 12)

def test_plots() :
    plots = ising.thermo.PlotValsMethod.getsingleton()
    plots.setstrat(ising.thermo.SequentialStrategy.getsingleton())
    ham = ising.hamiltonian.PeriodicHamiltonian(__J, __M)
    points = list(np.linspace(0.1, 20))
    assert(type(plots.getstrat()) == ising.thermo.SequentialStrategy)
    seq_e, seq_h, seq_m = plots.calc_plot_vals(ham, __length, points, __k)
    plots.setstrat(ising.thermo.ThreadedStrategy.getsingleton())
    thr_e, thr_h, thr_m = plots.calc_plot_vals(ham, __length, points, __k)
    plots.setstrat(ising.fastcwrapper.CPlotStrategy.getsingleton())
    cpl_e, cpl_h, cpl_m = plots.calc_plot_vals(ham, __length, points, __k)
    assert(all(map(lambda s, t, c: abs(s - c) <= 1e-4 and abs(t - c) <= 1e-4,
                   seq_e, thr_e, cpl_e)))
    assert(all(map(lambda s, t, c: abs(s - c) <= 1e-4 and abs(t - c) <= 1e-4,
                   seq_h, thr_h, cpl_h)))
    assert(all(map(lambda s, t, c: abs(s - c) <= 1e-4 and abs(t - c) <= 1e-4,
                   seq_m, thr_m, cpl_m)))
    
