#!/usr/bin/python3

import sys

try :
    from . import hamiltonian
    from . import thermo
    from . import constants
    from . import spins
except ImportError :
    import hamiltonian
    import thermo
    import constants
    import spins

import concurrent.futures
import math
import os

class CThermoStrategy(thermo.ThermoStrategy) :
    def __init__(self) :
        super().__init__()
        self.__threads = max(32, 4 + os.cpu_count())

    def getthreads(self) :
        return self.__threads

    def setthreads(self, threads) :
        self.__threads = threads

    def partition(self, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float) :
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian) :
            return fastc.p_partition(length, hamilt.getcoupling(), hamilt.getmagnet(),
                                           temp, boltzmann, self.getthreads())
        else :
            return thermo.FullCalcStrategy.getsingleton().partition(hamilt, length,
                                                             temp, boltzmann)
        
    def average(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float, *args, **kwargs) :
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian) :
            return fastc.p_average(lambda sp: func(spins.SpinInteger(sp, length)), length, hamilt.getcoupling(), hamilt.getmagnet(),
                                           temp, boltzmann)
        else :
            return thermo.FullCalcStrategy.getsingleton().average(func, hamilt, length,
                                                             temp, boltzmann,
                                                           *args, **kwargs)

    def variance(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float, *args, **kwargs) :
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian) :
            return fastc.p_variance(lambda sp: func(spins.SpinInteger(sp, length)), length, hamilt.getcoupling(), hamilt.getmagnet(),
                                           temp, boltzmann)
        else :
            return thermo.FullCalcStrategy.getsingleton().variance(func, hamilt, length,
                                                             temp, boltzmann,
                                                           *args, **kwargs)
        

class CPlotStrategy(thermo.PlotValsStrategy) :
    def __init__(self) :
        super().__init__()
        self.__threads = max(32, 4 + os.cpu_count())

    def getthreads(self) :
        return self.__threads
    def setthreads(self, threads) :
        self.__threads = threads

    def calc_plot_vals(self, hamilt : hamiltonian.Hamiltonian, length,
                       temps, boltzmann) :
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian) :
            return fastc.p_plots(length, hamilt.getcoupling(), hamilt.getmagnet(), list(temps), boltzmann, self.getthreads())
        else :
            return super().calc_plot_vals(hamilt, length, temps, boltzmann);
 
try :
    from . import fastc
except ImportError :
    import fastc
