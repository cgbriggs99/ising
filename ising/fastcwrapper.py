#!/usr/bin/python3

import sys

try :
    from . import hamiltonian
    from . import thermo
    from . import constants
except ImportError :
    import hamiltonian
    import thermo
    import constants

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
            return fastc.fastc_p_partition(length, hamilt.getcoupling(), hamilt.getmagnet(),
                                           temp, boltzmann, self.getthreads())
        elif isinstance(hamilt, hamiltonian.NPHamiltonian) :
            return fastc.fastc_np_partition(length, hamilt.getcoupling(), hamilt.getmagnet(),
                                            temp, boltzmann, self.getthreads())
        elif isinstance(hamilt, hamiltonian.GraphHamiltonian) :
            return fastc.fastc_graph_partition(length, hamilt, temp, boltzmann, self.getthreads())
        else :
            return fastc.fastc_gen_partition(length, hamilt, temp, boltzmann, self.getthreads())
        
    def average(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float, *args, **kwargs) :
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian) :
            return fastc.fastc_p_average(lambda sp: func(sp, *args, **kwargs), length, hamilt.getcoupling(), hamilt.getmagnet(),
                                           temp, boltzmann, self.getthreads())
        elif isinstance(hamilt, hamiltonian.NPHamiltonian) :
            return fastc.fastc_np_average(lambda sp: func(sp, *args, **kwargs), length, hamilt.getcoupling(), hamilt.getmagnet(),
                                            temp, boltzmann, self.getthreads())
        elif isinstance(hamilt, hamiltonian.GraphHamiltonian) :
            return fastc.fastc_graph_average(lambda sp: func(sp, *args, **kwargs), length, hamilt, temp, boltzmann, self.getthreads())
        else :
            return fastc.fastc_gen_average(lambda sp: func(sp, *args, **kwargs), length, hamilt, temp, boltzmann, self.getthreads())

    def variance(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float, *args, **kwargs) :
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian) :
            return fastc.fastc_p_variance(lambda sp: func(sp, *args, **kwargs), length, hamilt.getcoupling(), hamilt.getmagnet(),
                                           temp, boltzmann, self.getthreads())
        elif isinstance(hamilt, hamiltonian.NPHamiltonian) :
            return fastc.fastc_np_variance(lambda sp: func(sp, *args, **kwargs), length, hamilt.getcoupling(), hamilt.getmagnet(),
                                            temp, boltzmann, self.getthreads())
        elif isinstance(hamilt, hamiltonian.GraphHamiltonian) :
            return fastc.fastc_graph_variance(lambda sp: func(sp, *args, **kwargs), length, hamilt, temp, boltzmann, self.getthreads())
        else :
            return fastc.fastc_gen_variance(lambda sp: func(sp, *args, **kwargs), length, hamilt, temp, boltzmann, self.getthreads())
        

class CPlotStrategy(thermo.ThreadedStrategy) :
    def __init__(self) :
        super().__init__()

    def calc_plot_vals(self, hamilt : hamiltonian.Hamiltonian, length,
                       temps, boltzmann) :
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian) :
            return fastc.fastc_p_plots(length, hamilt.getcoupling(), hamilt.getmagnet(), temps, boltzmann, self.getthreads())
        elif isinstance(hamilt, hamiltonian.NPHamiltonian) :
            return fastc.fastc_np_plots(length, hamilt.getcoupling(), hamilt.getmagnet(), temps, boltzmann, self.getthreads())
        elif isinstance(hamilt, hamiltonian.GraphHamiltonian) :
            return fastc.fastc_graph_plots(length, hamilt, temps, boltzmann, self.getthreads())
        else :
            return fastc.fastc_gen_plot(length, hamilt, temps, boltzmann, self.getthreads())

def plotvals(ham, length, temps, boltzmann = constants.BOLTZMANN_K,
                threads = max(32, 4 + os.cpu_count()), no_c = None) :
    """
    This is a wrapper for src.fastc.plot_vals that turns the temps into a list,
    and has default values for several parameters. Also works with Hamiltonian.
    """
    assert("ising.fastc" in sys.modules)
    if "ising.fastc" in sys.modules and (no_c is False or no_c is None):
        return fastc.plot_vals(length, ham.getcoupling(),
                              ham.getmagnet(), list(temps),
                              boltzmann, threads)
    else :
        exc = concurrent.futures.ThreadPoolExecutor(threads)
        out = (list(exc.map(lambda t: thermo.ThermoMethod.getsingleton().average(ham.energy, ham,
                                                length,temp = t,
                                                 boltzmann = boltzmann),
                           temps)), list(exc.map(lambda t: math.sqrt(thermo.ThermoMethod.getsingleton().variance(ham.energy, ham,
                                                  length, temp = t,
                                                  boltzmann = boltzmann)
                                   ) / (boltzmann * t ** 2),
                         temps)), list(exc.map(lambda t: math.sqrt(thermo.ThermoMethod.getsingleton().variance(
            lambda sc: sc.magnetization(), ham, length, temp = t,
            boltzmann = boltzmann)) / (boltzmann * t), temps)))
        exc.shutdown()
        return out
 
try :
    from . import fastc
except ImportError :
    import fastc
