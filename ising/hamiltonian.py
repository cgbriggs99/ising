#!/usr/bin/python3

# For the __main__.py module.
try :
    from . import constants
    from . import spins
    from . import graph
except ImportError :
    import constants
    import spins
    import graph

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
    def __init__(self) :
        pass

    def energy(self, spin : spins.SpinConfig) :
        raise NotImplemented()

    def temperature(self, spin : spins.SpinConfig,
                    boltzmann = constants.BOLTZMANN_K) :
        """
Finds E/k.

Parameters
spin: Spin configuration.
boltzmann: Value of the Boltzmann constant in whatever units.
"""
        return self.energy(spin) / boltzmann
    def energy_pos(self, spin : spins.SpinConfig, pos : int,
               boltzmann = ising.BOLTZMANN_K) :
        raise NotImplemented
    
class ConstantHamiltonian(Hamiltonian) :
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

class PeriodicHamiltonian(ConstantHamiltonian) :
    def __init__(self, coupling, magnet) :
        super().__init__(coupling, magnet)
        
    def energy(self, spin : spins.SpinConfig) :
        """
Find the raw energy of a spin configuration.
"""
        assert(isinstance(spin, spins.SpinConfig))
        return -self.getcoupling() * sum(spin[i - 1] * spin[i]
                                         for i in range(len(spin))) + \
                                         self.getmagnet() * sum(spin)

# Non-periodic boundary condition.
class NPHamiltonian(ConstantHamiltonian) :
    """
Represents a Hamiltonian with a non-periodic boundary condition.
"""
    def __init__(self, coupling, magnet) :
        super().__init__(coupling, magnet)

    def energy(self, spin : spins.SpinConfig) :
        """
Find the raw energy of a spin configuration.
"""
        return -self.getcoupling() * sum(spin[i] * spin[i + 1]
                                         for i in range(len(spin) - 1)) + \
                                         self.getmagnet() * sum(spin)
# Generalized boundary condition.
class GraphHamiltonian(Hamiltonian) :
    def __init__(self, conns : graph.Graph, mags) :
        """
The data argument for the vertces should be the index in the spin matrix it
corresponds with. The length of each edge should be the spin coupling constant.
mags here is either a list of magnet constants, or a single constant.
"""
        self.__graph = conns
        self.__mags = mags

    def getconns(self) :
        return self.__graph

    def getmagnet(self) :
        return self.__mags

    def setmagnet(self, mags) :
        self.__mags = mags
        return mags

    def energy(self, spin : spins.SpinConfig) :
        couple = 0
        for v in self.getconns().getverts() :
            neigh = self.getconns().getneighbors(v)
            print(neigh)
            for n in neigh :
                # Undirected edges end up being double counted. Don't do that.
                if n[2] :
                    couple += -n[1] / 2 * \
                              (spin[v.getdata()] * spin[n[0].getdata()])
                else :
                    couple += -n[1] * (spin[v.getdata()] * spin[n[0].getdata()])
                    
        if hasattr(self.getmagnet(), "__iter__") :
            try :
                mag = sum(spin[i] * self.getmagnet()[i] for i in range(len(spin)))
            except :
                raise Exception("The number of magnet constants needs to" +
                                " be the same as the number of spins.")
        else :
            mag = self.getmagnet() * sum(spin)
        print(couple)
        print(mag)
        return couple + mag
    
