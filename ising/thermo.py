#!/usr/bin/python3

from .ising import boltzmann_k
import math

def partition(hamiltonian : Hamiltonian, length, temp = 298.15,
              boltzmann = boltzmann_k) :
    """
Returns the value of the partition function for a Hamiltonian at a given
temperature and a boltzmann constant with given units.
"""
    return sum(math.exp(-hamiltonian.energy(SpinInteger(sp, length)) /
                        (boltzmann * temp)) for sp in range(2 ** length))

def average_value(func, hamiltonian : Hamiltonian, length, temp = 298.15,
                  boltzmann = boltzmann_k, *args, **kwargs) :
    """
Find the value of an intrinsic property normalized by the partition function.
"""
    return sum(func(sp, *args, *kwargs) *
               math.exp(-hamiltonian.energy(SpinInteger(sp, length)) / \
                                            (boltzmann * temp))
               for sp in range(2 ** length)) / partition(hamiltonian, length,
                                                         temp, boltzmann)
def variance(func, hamiltonian : Hamiltonian, length, temp = 298.15,
          boltzmann = boltzmann_k, *args, **kwargs) :
    """
Find the variance of an intrinsic property normalized by the partition function.
"""
    return (sum(func(sp, *args, **kwargs) ** 2 *
               math.exp(-hamiltonian.energy(SpinInteger(sp, length)) / \
                        (boltzmann * temp)) for sp in range(2 ** length)) - \
            sum(func(sp, *args, **kwargs) *
                math.exp(-hamiltonian.energy(SpinInteger(sp, length)) / \
                         (boltzmann * temp))
                for sp in range(2 ** length)) ** 2) / partition(hamiltonian,
                                                                length, temp,
                                                                boltzmann)
