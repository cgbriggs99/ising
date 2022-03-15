#!/usr/bin/python3

"""
Contains the Boltzmann constant.
"""
BOLTZMANN_K = 1.38064852e-23 # J/K

try :
    from . import hamiltonian
except ImportError :
    import hamiltonian

try :
    from .src import fafb
except ImportError :
    try :
        import src.fafb
    except ImportError :
        pass;

import os
import sys
import concurrent.futures


def fafbwrapper(hamiltonian, length, temps, boltzmann = BOLTZMANN_K,
                threads = max(32, 4 + os.cpu_count())) :
    """
    This is a wrappr for src.fafb.plot_vals that turns the temps into a list,
    and has default values for several parameters. Also works with Hamiltonian.
    """
    if "src" in sys.modules :
        return src.fafb.plot_vals(length, hamiltonian.getcoupling(),
                              hamiltonian.getmagnet(), list(temps),
                              boltzmann, threads)
    else :
        exc = concurrent.futures.ThreadPoolExecutor(threads)
        out = (list(exc.map(lambda t: thermo.average_value(ham.energy, ham,
                                                length,temp = t,
                                                 boltzmann = boltzmann),
                           temps)), list(exc.map(lambda t: math.sqrt(thermo.variance(ham.energy, ham,
                                                  length, temp = t,
                                                  boltzmann = boltzmann)
                                   ) / (argsboltzmann * t ** 2),
                         temps)), list(exc.map(lambda t: math.sqrt(thermo.variance(
            lambda sc: sc.magnetization(), ham, length, temp = t,
            boltzmann = boltzmann)) / (boltzmann * t), temps)))
        exc.shutdown()
        return out
