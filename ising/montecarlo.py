#!/usr/bin/python3

try :
    from . import hamiltonian
    from . import spins
    from . import thermo
except ImportError :
    import hamiltonian
    import spins
    import thermo

import math
import random

class RandomIterator :
    def __init__(self, *args) :
        self.__curr = 0
        if len(args) == 2 :
            self.__start = 0
            self.__end = args[1]
            self.__length = args[0]
            self.__step = 1
        elif len(args) == 3 :
            self.__start = args[1]
            self.__end = args[2]
            self.__length = args[0]
            self.__step = 1
        elif len(args) == 4 :
            self.__start = args[1]
            self.__end = args[2]
            self.__length = args[0]
            self.__step = args[4]
        else :
            raise TypeError
        assert(self.__length > 0)
    def __iter__(self) :
        return self
    def __next__(self) :
        if self.__curr >= self.__length :
            raise StopIteration
        self.__curr += 1
        return random.randrange(self.__start, self.__end, self.__step)
    

class MonteCarloStrategy(thermo.ThermoStrategy) :
    def __init__(self) :
        super().__init__()
        self.__montecarlo = 1000

    def setpoints(self, points) :
        self.__montecarlo = points

    def getpoints(self) :
        return self.__montecarlo

    def partition(self, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float) :
        return 1

    def average(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                temp : float, boltzmann : float, *args, **kwargs) :
        total = 0
        den = 0
        for i in RandomIterator(self.__montecarlo, 2 ** length) :
            sp = spins.SpinInteger(i, length)
            total += func(sp, *args, **kwargs) * \
                     math.exp(-hamilt.energy(sp) / (boltzmann * temp))
            den += math.exp(-hamilt.energy(sp) / (boltzmann * temp))
        return (total / den)
        
    def variance(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                 temp : float, boltzmann : float, *args, **kwargs) :
        total1 = 0
        total2 = 0
        den = 0
        for i in RandomIterator(self.__montecarlo, 2 ** length) :
            sp = spins.SpinInteger(i, length)
            total1 += func(sp, *args, **kwargs) * \
                      math.exp(-hamilt.energy(sp) / (boltzmann * temp))
            total2 += func(sp, *args, **kwargs) ** 2 * \
                      math.exp(-hamilt.energy(sp) / (boltzmann * temp))
            den += math.exp(-hamilt.energy(sp) / (boltzmann * temp))
        return (total2 / den - (total1 / den) ** 2)
        
class MetropolisStrategy(thermo.ThermoStrategy) :
    def __init__(self) :
        super().__init__()
        self.__metropolis = 1000
        self.__depth = 10

    def getdepth(self) :
        return self.__depth
    def getpoints(self) :
        return self.__metropolis
    def setdepth(self, depth) :
        self.__depth = depth
    def setpoints(self, points) :
        self.__metropolis = points

    def partition(self, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float) :
        return 1

    def average(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                temp : float, boltzmann : float, *args, **kwargs) :
        total = 0
        den = 0
        for i in RandomIterator(self.__metropolis, 2 ** length) :
            sp = spins.SpinInteger(i, length)
            energy = hamilt.energy(sp) / (boltzmann * temp)
            total += func(sp, *args, **kwargs) * math.exp(-energy)
            den += math.exp(-energy)
            for _ in range(self.__depth) :
                for j in range(length) :
                    sp2 = sp.copy()
                    sp2.flipbit(j)
                    en2 = hamilt.energy(sp) / (boltzmann * temp)
                    diff = energy - en2
                    total += func(sp2, *args, **kwargs) * math.exp(-en2)
                    den += math.exp(-en2)
                    if energy < en2 :
                        energy = en2
                        sp = sp2
                        break
                    else :
                        #ln a = diff
                        #u in [0, 1]
                        #ln u in (-inf, 0)
                        if random.random() < math.exp(diff) :
                            energy = en2
                            sp = sp2
                            break
                        else :
                            continue
        return total / den

    def variance(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                 temp : float, boltzmann : float, *args, **kwargs) :
        total1 = 0
        total2 = 0
        den = 0
        for i in RandomIterator(self.__metropolis, 2 ** length) :
            sp = spins.SpinInteger(i, length)
            energy = hamilt.energy(sp) / (boltzmann * temp)
            total1 += func(sp, *args, **kwargs) * math.exp(-energy)
            total2 += func(sp, *args, **kwargs) ** 2 * math.exp(-energy)
            den += math.exp(-energy)
            for _ in range(self.__depth) :
                for j in range(length) :
                    sp2 = sp.copy()
                    sp2.flipbit(j)
                    en2 = hamilt.energy(sp) / (boltzmann * temp)
                    diff = energy - en2
                    total1 += func(sp2, *args, **kwargs) * math.exp(-en2)
                    total2 += func(sp2, *args, **kwargs) ** 2 * math.exp(-en2)
                    den += math.exp(-en2)
                    if energy < en2 :
                        energy = en2
                        sp = sp2
                        break
                    else :
                        #ln a = diff
                        #u in [0, 1]
                        #ln u in (-inf, 0)
                        if random.random() < math.exp(diff) :
                            energy = en2
                            sp = sp2
                            break
                        else :
                            continue
        return total2 / den - (total1 / den) ** 2
                            
            
