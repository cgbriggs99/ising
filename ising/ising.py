#!/usr/bin/python3

"""
Contains the Boltzmann constant.
"""
BOLTZMANN_K = 1.38064852e-23 # J/K

try :
    from . import hamiltonian
    from . import thermo
except ImportError :
    import hamiltonian
    import thermo

try :
    from .src import fastc
except ImportError :
    try :
        import src.fastc
    except ImportError :
        pass;

import os
import sys
import concurrent.futures
import math


def fastcwrapper(ham, length, temps, boltzmann = BOLTZMANN_K,
                threads = max(32, 4 + os.cpu_count()), no_c = None) :
    """
    This is a wrapper for src.fastc.plot_vals that turns the temps into a list,
    and has default values for several parameters. Also works with Hamiltonian.
    """
    assert("ising.src.fastc" in sys.modules)
    if "ising.src.fastc" in sys.modules and (no_c is False or no_c is None):
        return fastc.plot_vals(length, ham.getcoupling(),
                              ham.getmagnet(), list(temps),
                              boltzmann, threads)
    else :
        exc = concurrent.futures.ThreadPoolExecutor(threads)
        out = (list(exc.map(lambda t: thermo.average_value(ham.energy, ham,
                                                length,temp = t,
                                                 boltzmann = boltzmann),
                           temps)), list(exc.map(lambda t: math.sqrt(thermo.variance(ham.energy, ham,
                                                  length, temp = t,
                                                  boltzmann = boltzmann)
                                   ) / (boltzmann * t ** 2),
                         temps)), list(exc.map(lambda t: math.sqrt(thermo.variance(
            lambda sc: sc.magnetization(), ham, length, temp = t,
            boltzmann = boltzmann)) / (boltzmann * t), temps)))
        exc.shutdown()
        return out
