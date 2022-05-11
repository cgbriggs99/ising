#!/usr/bin/python3

"""
ising.hamiltonian

Holds various kinds of Hamiltonians.
"""

# For the __main__.py module.
try:
    from . import constants
    from . import spins
    from . import graph
except ImportError:
    import constants
    import spins
    import graph


class Hamiltonian:
    """
Represents the base Hamiltonian.
"""

    def energy(self, spin: spins.SpinConfig):
        """
Returns the energy of a configuration under the hamiltonian.
"""
        raise NotImplementedError

    def temperature(self, spin: spins.SpinConfig, boltzmann=constants.BOLTZMANN_K):
        """
Finds E/k.

Parameters
spin: Spin configuration.
boltzmann: Value of the Boltzmann constant in whatever units.
"""
        return self.energy(spin) / boltzmann


class ConstantHamiltonian(Hamiltonian):
    """
Represents a Hamiltonian for an Ising system.
"""

    def __init__(self, coupling, magnet):
        self._coupling = coupling
        self._mag = magnet

    def getcoupling(self):
        """
Gets the value of the spin coupling constant.
"""
        return self._coupling

    def getmagnet(self):
        """
Gets the value of the magnetization.
"""
        return self._mag

    def setcoupling(self, value):
        """
Sets the value of the spin coupling constant.
"""
        self._coupling = value
        return value

    def setmagnet(self, value):
        """
Sets the value of the magnetization.
"""
        self._mag = value
        return value

    def energy(self, spin: spins.SpinConfig):
        raise NotImplementedError


class PeriodicHamiltonian(ConstantHamiltonian):
    """
Represents a system with periodic boundary conditions.
"""

    def energy(self, spin: spins.SpinConfig):
        """
Find the raw energy of a spin configuration.
"""
        assert isinstance(spin, spins.SpinConfig)
        return -self.getcoupling() * sum(
            spin[i - 1] * spin[i] for i in range(len(spin))
        ) + self.getmagnet() * sum(spin)


# Non-periodic boundary condition.
class NPHamiltonian(ConstantHamiltonian):
    """
Represents a Hamiltonian with a non-periodic boundary condition.
"""

    def energy(self, spin: spins.SpinConfig):
        return -self.getcoupling() * sum(
            spin[i] * spin[i + 1] for i in range(len(spin) - 1)
        ) + self.getmagnet() * sum(spin)


# Generalized boundary condition.
class GraphHamiltonian(Hamiltonian):
    """
Represents a Hamiltonian with general interactions between states.
"""

    def __init__(self, conns: graph.Graph, mags):
        """
The data argument for the vertces should be the index in the spin matrix it
corresponds with. The length of each edge should be the spin coupling constant.
mags here is either a list of magnet constants, or a single constant.
"""
        self._graph = conns
        self._mags = mags

    def getconns(self):
        """
Gets the underlying graph.
"""
        return self._graph

    def getmagnet(self):
        """
Gets the list of magnetization strengths
"""
        return self._mags

    def setmagnet(self, mags):
        """
Sets the list of magnetization strengths.
"""
        self._mags = mags
        return mags

    def energy(self, spin: spins.SpinConfig):
        couple = 0
        for vert in self.getconns().getverts():
            neigh = self.getconns().getneighbors(vert)
            print(neigh)
            for nei in neigh:
                # Undirected edges end up being double counted. Don't do that.
                if nei[2]:
                    couple += (
                        -nei[1] / 2 * (spin[vert.getdata()] * spin[nei[0].getdata()])
                    )
                else:
                    couple += -nei[1] * (spin[vert.getdata()] * spin[nei[0].getdata()])

        if hasattr(self.getmagnet(), "__iter__"):
            try:
                mag = sum(spin[i] * self.getmagnet()[i] for i in range(len(spin)))
            except Exception as exc:
                raise Exception(
                    "The number of magnet constants needs to"
                    + " be the same as the number of spins."
                ) from exc
        else:
            mag = self.getmagnet() * sum(spin)
        print(couple)
        print(mag)
        return couple + mag
