#!/usr/bin/python3

from .ising import boltzmann_k
import .spins

class Hamiltonian :
    """
Represents a Hamiltonian for an Ising system.
"""
    def __init__(self, coupling, magnet) :
        self.__coupling = coupling
        self.__mag = magnet
    def getcoupling(self) :
        return self.__coupling
    def getmagnet(self) :
        return self.__mag
    def setcoupling(self, value) :
        self.__coupling = value
    def setmagnet(self, value) :
        self.__mag = value
    def energy(self, spin : SpinConfig) :
        """
Find the raw energy of a spin configuration. Uses the formula
$$-J \sum_{i} S_i S_{i+1} + \mu \sum_i S_i$$
"""
        return -self.getcoupling() * sum(spin[i - 1] * spin[i]
                                         for i in range(len(spin))) + \
                                         self.getmagnet() * sum(spin)
    def temperature(self, spin : SpinConfig, boltzmann = boltzmann_k) :
        """
Finds E/k.

Parameters
spin: Spin configuration.
boltzmann: Value of the Boltzmann constant in whatever units.
"""
        return self.energy(spin) / boltzmann
