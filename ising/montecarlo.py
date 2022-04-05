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

class MonteCarloStrategy(thermo.ThermoStrategy) :
    def __init__(self) :
        super().__init__()
        self.__montecarlo = 1000

    def partition(self, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float) :
        return self.__montecarlo * length

    def average(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                temp : float, boltzmann : float) :
        
