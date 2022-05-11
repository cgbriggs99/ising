#!/usr/bin/python3

import math
try :
    from . import constants
    from . import hamiltonian
    from . import spins
    from . import despats
except ImportError :
    import constants
    import hamiltonian
    import spins
    import despats.singleton
import os
import math
import concurrent.futures

class ThermoStrategy(despats.singleton.Singleton) :
    def __init__(self) :
        super().__init__()

    def partition(self, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float) :
        raise NotImplemented

    def average(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                temp : float, boltzmann : float, *args, **kwargs) :
        raise NotImplemented

    def variance(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                 temp : float, boltzmann : float, *args, **kwargs) :
        raise NotImplemented

class ThermoMethod(despats.singleton.Singleton) :
    def __init__(self) :
        self.__strat = FullCalcStrategy.getsingleton()
        
    def setstrat(self, strat : ThermoStrategy) :
        self.__strat = strat

    def getstrat(self) :
        return self.__strat

    def partition(self, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp = 298.15, boltzmann = constants.BOLTZMANN_K) :
        return self.__strat.partition(hamilt, length, temp, boltzmann)
    
    def average(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp = 298.15, boltzmann = constants.BOLTZMANN_K,
                *args, **kwargs) :
        return self.__strat.average(func, hamilt, length, temp, boltzmann,
                                    *args, **kwargs)
    
    def variance(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp = 298.15, boltzmann = constants.BOLTZMANN_K,
                 *args, **kwargs) :
        return self.__strat.variance(func, hamilt, length, temp, boltzmann,
                                      *args, **kwargs)

    def energy(self, hamilt : hamiltonian.Hamiltonian, length : int,
               temp = 298.15, boltzmann = constants.BOLTZMANN_K) :
        return self.__strat.average(hamilt.energy, length, temp, boltzmann)

    def heatcap(self, hamilt : hamiltonian.Hamiltonian, length : int,
                temp = 298.15, boltzmann = constants.BOLTZMANN_K) :
        return math.sqrt(self.__strat.variance(hamilt.energy, hamilt, length,
                                               temp, boltzmann)) / \
                                               (boltzmann * temp ** 2)

    def magneticsus(self, hamilt : hamiltonian.Hamiltonian, length : int,
                    temp = 298.15, boltzmann = constants.BOLTZMANN_K) :
        return math.sqrt(self.__strat.variance(lambda sc : sc.magnetization(),
                                               hamilt, length,
                                               temp, boltzmann)) / \
                                               (boltzmann * temp)

class PlotValsStrategy(despats.singleton.Singleton) :
    def __init__(self) :
        super().__init__()

    def calc_plot_vals(self, hamilt : hamiltonian.Hamiltonian, length,
                       temps, boltzmann) :
        raise NotImplemented

class SequentialStrategy(PlotValsStrategy) :
    def __init__(self) :
        super().__init__()

    def calc_plot_vals(self, hamilt : hamiltonian.Hamiltonian, length,
                       temps, boltzmann) :
        return (list(map(lambda t : ThermoMethod.getsingleton().energy(hamilt,
                         length, t, boltzmann), temps)),
                list(map(lambda t : ThermoMethod.getsingleton().heatcap(hamilt,
                         length, t, boltzmann), temps)),
                list(map(lambda t : ThermoMethod.getsingleton().magneticsus(
                    hamilt, length, t, boltzmann), temps)))

class ThreadedStrategy(PlotValsStrategy) :
    def __init__(self) :
        super().__init__()
        self.__threads = max(32, 4 + os.cpu_count())

    def getthreads(self) :
        return self.__threads
    def setthreads(self, threads) :
        self.__threads = threads

    def calc_plot_vals(self, hamilt : hamiltonian.Hamiltonian, length,
                       temps, boltzmann)
    exc = concurrent.futures.ThreadPoolExecutor(self.getthreads())
    out = (list(exc.map(lambda t : ThermoMethod.getsingleton().energy(hamilt,
                         length, t, boltzmann), temps)),
            list(exc.map(lambda t : ThermoMethod.getsingleton().heatcap(hamilt,
                         length, t, boltzmann), temps)),
            list(exc.map(lambda t : ThermoMethod.getsingleton().magneticsus(
                    hamilt, length, t, boltzmann), temps)))
    exc.shutdown()
    return out

class PlotValsMethod(despats.singleton.Singleton) :
    def __init__(self) :
        super().__init__()
        self.__strat = ThreadedStrategy.getsingleton() 

    def getstrat(self) :
        return self.__strat

    def setstrat(self, strat) :
        self.__strat = strat

    def calc_plot_vals(self, hamilt : hamiltonian.Hamiltonian, length,
                       temps, boltzmann = constants.BOLTZMANN_K) :
        return self.__strat.calc_plot_vals(hamilt, length, temps, boltzmann)

class FullCalcStrategy(ThermoStrategy) :
    def __init__(self) :
        super().__init__()

    def partition(self, hamilt : hamiltonian.Hamiltonian, length : int,
                  temp : float, boltzmann : float) :
        """
Returns the value of the partition function for a Hamiltonian at a given
temperature and a boltzmann constant with given units.
"""
        return sum(math.exp(-hamilt.energy(spins.SpinInteger(sp, length)) /
                            (boltzmann * temp)) for sp in range(2 ** length))

    def average(self, func, hamilt : hamiltonian.Hamiltonian,
                      length : int, temp : float, boltzmann : float,
                      *args, **kwargs) :
        """
Find the value of an intrinsic property normalized by the partition function.
"""
    
        return sum(func(spins.SpinInteger(sp, length), *args, *kwargs) *
                   math.exp(-hamilt.energy(spins.SpinInteger(sp, length)) / \
                                                (boltzmann * temp))
                   for sp in range(2 ** length)) / self.partition(hamilt, length,
                                                             temp, boltzmann)

    def variance(self, func, hamilt : hamiltonian.Hamiltonian, length : int,
                 temp : float, boltzmann :float, *args, **kwargs) :
        """
Find the variance of an intrinsic property normalized by the partition function.
"""
        part = self.partition(hamilt, length, temp, boltzmann)
        out = sum(func(spins.SpinInteger(sp, length), *args, **kwargs) ** 2 *
                   math.exp(-hamilt.energy(spins.SpinInteger(sp, length)) / \
                            (boltzmann * temp)) for sp in range(2 ** length)) /\
                            part - \
                sum(func(spins.SpinInteger(sp, length), *args, **kwargs) *
                    math.exp(-hamilt.energy(spins.SpinInteger(sp, length)) / \
                             (boltzmann * temp))
                    for sp in range(2 ** length)) ** 2 / part ** 2
        return out
