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
