#!/usr/bin/python3

import math
try :
    from . import ising
    from . import hamiltonian
    from . import spins
except ImportError :
    import ising
    import hamiltonian
    import spins


def partition(hamilt : hamiltonian.Hamiltonian, length, temp = 298.15,
              boltzmann = ising.BOLTZMANN_K) :
    """
Returns the value of the partition function for a Hamiltonian at a given
temperature and a boltzmann constant with given units.
"""
    return sum(math.exp(-hamilt.energy(spins.SpinInteger(sp, length)) /
                        (boltzmann * temp)) for sp in range(2 ** length))

def average_value(func, hamilt : hamiltonian.Hamiltonian, length, temp = 298.15,
                  boltzmann = ising.BOLTZMANN_K, *args, **kwargs) :
    """
Find the value of an intrinsic property normalized by the partition function.
"""
    
    return sum(func(spins.SpinInteger(sp, length), *args, *kwargs) *
               math.exp(-hamilt.energy(spins.SpinInteger(sp, length)) / \
                                            (boltzmann * temp))
               for sp in range(2 ** length)) / partition(hamilt, length,
                                                         temp, boltzmann)

def variance(func, hamilt : hamiltonian.Hamiltonian, length, temp = 298.15,
          boltzmann = ising.BOLTZMANN_K, *args, **kwargs) :
    """
Find the variance of an intrinsic property normalized by the partition function.
"""
    part = partition(hamilt, length, temp, boltzmann)
    out = sum(func(spins.SpinInteger(sp, length), *args, **kwargs) ** 2 *
               math.exp(-hamilt.energy(spins.SpinInteger(sp, length)) / \
                        (boltzmann * temp)) for sp in range(2 ** length)) /\
                        part - \
            sum(func(spins.SpinInteger(sp, length), *args, **kwargs) *
                math.exp(-hamilt.energy(spins.SpinInteger(sp, length)) / \
                         (boltzmann * temp))
                for sp in range(2 ** length)) ** 2 / part ** 2
    return out
