#!/usr/bin/python3

import numpy as np

"""
Computes properties of Ising systems.
"""

boltzmann_k = 1.38064852e-23 # J/K

class SpinConfig :
    """
Represents an abstract spin configuration.
"""
    def __init__(self) :
        pass
    def __len__(self) :
        pass
    def __getitem__(self, index) :
        pass
    def __setitem__(self, index) :
        pass
    def __iter__(self, index, value) :
        pass
    def __str__(self) :
        """
Returns a representation using spin arrows for this object.
"""
        return "".join(['↿' if i == 1 else '⇂' for i in self])

class SpinMatrix(SpinConfig) :
    """
Represents a spin configuration set up with a set of 1's and -1's representing
spins.
"""
    def __init__(self, data) :
        self.__data = list(data)
    def __len__(self) :
        return len(self.__data)
    def __getitem__(self, index) :
        return self.__data[index]
    def __setitem__(self, index, value) :
        self.__data[index] = value
        return value
    def __iter__(self) :
        return iter(self.__data)
class SpinInteger(SpinConfig) :
    """
Represents a spin configuration determined from the binary representation of
an integer.
"""
    def __init__(self, numeral, length) :
        self.__numeral = numeral
        self.__len = length
    def __len__(self) :
        return self.__len
    def __getitem__(self, index) :
        assert(index >= 0 and index < self.__len)
        return 2 * (self.__numeral & (1 << index)) - 1
    def __setitem__(self, index, value) :
        self.__numeral = (self.__numeral & ~(1 << index)) | \
                         (((value + 1) // 2) << index)
        return (value + 1) // 2
    def __iter__(self) :
        return _SpinIntegerIterator(self)
    def copy(self) :
        return SpinInteger(self.__numeral, self.__len)

class _SpinIntegerIterator :
    """
Iterator class for spins based on integers.
"""
    def __init__(self, other) :
        self.__index = 0
        self.__spi = other.copy()
    def __iter__(self) :
        return self
    def __next__(self) :
        if self.__index >= len(self.__spi) :
            raise StopIteration
        else :
            out = self.__spi[self.__index]
            self.__index += 1
            return out

class Hamiltonian :
    """
Represents a Hamiltonian for an Ising system.
"""
    def 


if __name__ == "__main__":
    import matplotlib.pyplot as plot
