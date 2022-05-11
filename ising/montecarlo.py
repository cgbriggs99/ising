#!/usr/bin/python3

"""
Contains classes for Monte-Carlo simulations.
"""

try:
    from . import hamiltonian
    from . import spins
    from . import thermo
except ImportError:
    import hamiltonian
    import spins
    import thermo

import math
import random


class RandomIterator:
    """
Represents an iterator over random numbers within a range.
"""

    def __init__(self, *args):
        self.__curr = 0
        if len(args) == 2:
            self.__start = 0
            self.__end = args[1]
            self.__length = args[0]
            self.__step = 1
        elif len(args) == 3:
            self.__start = args[1]
            self.__end = args[2]
            self.__length = args[0]
            self.__step = 1
        elif len(args) == 4:
            self.__start = args[1]
            self.__end = args[2]
            self.__length = args[0]
            self.__step = args[4]
        else:
            raise TypeError
        assert self.__length > 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__curr >= self.__length:
            raise StopIteration
        self.__curr += 1
        return random.randrange(self.__start, self.__end, self.__step)


class MonteCarloStrategy(thermo.ThermoStrategy):
    """
Represents a naïve implementation of the Monte-Carlo simulation.
"""

    def __init__(self):
        super().__init__()
        self._montecarlo = 1000

    def setpoints(self, points):
        """
Sets the number of points.
"""
        self._montecarlo = points

    def getpoints(self):
        """
Gets the number of points.
"""
        return self._montecarlo

    def partition(
        self,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
    ):
        """
Calculates the partition function.
"""
        raise NotImplementedError

    def average(
        self,
        func,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
        *args,
        **kwargs
    ):
        """
Calculates the average value of a function weighted with the Boltzmann distribution.
"""
        total = 0
        den = 0
        for i in RandomIterator(self._montecarlo, 2 ** length):
            spin = spins.SpinInteger(i, length)
            total += func(spin, *args, **kwargs) * math.exp(
                -hamilt.energy(spin) / (boltzmann * temp)
            )
            den += math.exp(-hamilt.energy(spin) / (boltzmann * temp))
        return total / den

    def variance(
        self,
        func,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
        *args,
        **kwargs
    ):
        """
Calculates the variance of a function weighted with the Boltzmann distribution.
"""
        total1 = 0
        total2 = 0
        den = 0
        for i in RandomIterator(self._montecarlo, 2 ** length):
            spin = spins.SpinInteger(i, length)
            total1 += func(spin, *args, **kwargs) * math.exp(
                -hamilt.energy(spin) / (boltzmann * temp)
            )
            total2 += func(spin, *args, **kwargs) ** 2 * math.exp(
                -hamilt.energy(spin) / (boltzmann * temp)
            )
            den += math.exp(-hamilt.energy(spin) / (boltzmann * temp))
        return total2 / den - (total1 / den) ** 2


class MetropolisStrategy(thermo.ThermoStrategy):
    """
Implementation of Metropolis sampling.
"""

    def __init__(self):
        super().__init__()
        self._metropolis = 1000
        self._depth = 10

    def getdepth(self):
        """
Gets the chain depth.
"""
        return self._depth

    def getpoints(self):
        """
Gets the number of seed points.
"""
        return self._metropolis

    def setdepth(self, depth):
        """
Sets the chain depth.
"""
        self._depth = depth

    def setpoints(self, points):
        """
Sets the number of seed points.
"""
        self._metropolis = points

    def partition(
        self,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
    ):
        """
Calculates the partition function.
"""
        raise NotImplementedError

    def average(
        self,
        func,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
        *args,
        **kwargs
    ):
        """
Calculates the average value of a function weighted with the Boltzmann distribution.
"""
        if length < self.getpoints():
            points = length
        else:
            points = self.getpoints()
        total = 0
        den = 0
        for i in RandomIterator(points, 2 ** length):
            spin = spins.SpinInteger(i, length)
            energy = hamilt.energy(spin) / (boltzmann * temp)
            total += func(spin, *args, **kwargs) * math.exp(-energy)
            den += math.exp(-energy)
            for _ in range(self._depth):
                for j in range(length):
                    spin2 = spin.copy()
                    spin2.flipbit(j)
                    ener2 = hamilt.energy(spin) / (boltzmann * temp)
                    diff = energy - ener2
                    total += func(spin2, *args, **kwargs) * math.exp(-ener2)
                    den += math.exp(-ener2)
                    if energy < ener2:
                        energy = ener2
                        spin = spin2
                        break
                    if random.random() < math.exp(diff):
                        energy = ener2
                        spin = spin2
                        break
        return total / den

    def variance(
        self,
        func,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
        *args,
        **kwargs
    ):
        """
Calculates the variance of a function weighted with the Boltzmann distribution.
"""
        if length < self.getpoints():
            points = length
        else:
            points = self.getpoints()
        total1 = 0
        total2 = 0
        den = 0
        for i in RandomIterator(points, 2 ** length):
            spin = spins.SpinInteger(i, length)
            energy = hamilt.energy(spin) / (boltzmann * temp)
            total1 += func(spin, *args, **kwargs) * math.exp(-energy)
            total2 += func(spin, *args, **kwargs) ** 2 * math.exp(-energy)
            den += math.exp(-energy)
            for _ in range(self._depth):
                for j in range(length):
                    spin2 = spin.copy()
                    spin2.flipbit(j)
                    ener2 = hamilt.energy(spin) / (boltzmann * temp)
                    diff = energy - ener2
                    total1 += func(spin2, *args, **kwargs) * math.exp(-ener2)
                    total2 += func(spin2, *args, **kwargs) ** 2 * math.exp(-ener2)
                    den += math.exp(-ener2)
                    if energy < ener2:
                        energy = ener2
                        spin = spin2
                        break
                    if random.random() < math.exp(diff):
                        energy = ener2
                        spin = spin2
                        break
        return total2 / den - (total1 / den) ** 2
