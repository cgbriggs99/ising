#!/usr/bin/python3

# For the __main__.py module.
try :
    from . import constants
    from . import spins
except ImportError :
    import constants
    import spins

####################################
#   mmmmmmm  mmmm  mmmm    mmmm    #
#      #    m"  "m #   "m m"  "m   #
#      #    #    # #    # #    #   #
#      #    #    # #    # #    #   #
#      #     #mm#  #mmm"   #mm#    #
####################################
# Distinguish between periodic boundary and non-periodic boundary. Perhaps
# also have a general graph version.
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
        return value
    def setmagnet(self, value) :
        self.__mag = value
        return value
    def energy(self, spin : spins.SpinConfig) :
        """
Find the raw energy of a spin configuration.
"""
        assert(isinstance(spin, spins.SpinConfig))
        return -self.getcoupling() * sum(spin[i - 1] * spin[i]
                                         for i in range(len(spin))) + \
                                         self.getmagnet() * sum(spin)
    def temperature(self, spin : spins.SpinConfig,
                    boltzmann = constants.BOLTZMANN_K) :
        """
Finds E/k.

Parameters
spin: Spin configuration.
boltzmann: Value of the Boltzmann constant in whatever units.
"""
        return self.energy(spin) / boltzmann
