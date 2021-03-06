#!/usr/bin/python3

"""
Contains several spin representations.
"""


class SpinConfig:
    """
Represents an abstract spin configuration.
"""

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError

    def __setitem__(self, index, value):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __str__(self):
        """
Returns a representation using spin arrows for this object.
"""
        return "".join(["↿" if i == 1 else "⇂" for i in self])

    def magnetization(self):
        """
Finds the spin excess of a spin configuration.
"""
        return len(list(filter(lambda x: x == 1, self))) - len(
            list(filter(lambda x: x == -1, self))
        )


class SpinMatrix(SpinConfig):
    """
Represents a spin configuration set up with a set of 1's and -1's representing
spins.
"""

    def __init__(self, data):
        self.__data = list(data)

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, index):
        index = index % len(self)
        return self.__data[index]

    def __setitem__(self, index, value):
        index = index % len(self)
        self.__data[index] = value
        return value

    def __iter__(self):
        return iter(self.__data)


class SpinInteger(SpinConfig):
    """
Represents a spin configuration determined from the binary representation of
an integer.
"""

    def __init__(self, numeral, length):
        self.__numeral = numeral
        self.__len = length

    def __len__(self):
        return self.__len

    def __getitem__(self, index):
        ind = index % len(self)
        if ind < 0:
            ind += len(self)
        return (
            2
            * (
                (self.__numeral & (1 << (self.__len - ind - 1)))
                >> (self.__len - ind - 1)
            )
            - 1
        )

    def __setitem__(self, index, value):
        ind = index % len(self)
        if ind < 0:
            ind += len(self)
        self.__numeral = (self.__numeral & ~(1 << (self.__len - ind - 1))) | (
            ((value + 1) // 2) << (self.__len - ind - 1)
        )
        return (value + 1) // 2

    def flipbit(self, index):
        """
Flips the spin at a given position.
"""
        self[index] = 1 - self[index]

    def __iter__(self):
        return _SpinIntegerIterator(self)

    def copy(self):
        """
Copies the current spin configuration.
"""
        return SpinInteger(self.__numeral, self.__len)

    def to_int(self):
        """
Returns the integer representation of the spin configuration.
"""
        return self.__numeral


class _SpinIntegerIterator:
    """
Iterator class for spins based on integers.
"""

    def __init__(self, other):
        self.__index = 0
        self.__spi = other.copy()

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index >= len(self.__spi):
            raise StopIteration
        out = self.__spi[self.__index]
        self.__index += 1
        return out
