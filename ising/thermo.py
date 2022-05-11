#!/usr/bin/python3

"""
Contains thermodynamic calculations.
"""

try:
    from . import constants
    from . import hamiltonian
    from . import spins
    from . import despats
except ImportError:
    import constants
    import hamiltonian
    import spins
    import despats.singleton
import os
import math
import concurrent.futures


class ThermoStrategy(despats.singleton.Singleton):
    """
Represents the base strategy for calculations.
"""

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
        **kwargs,
    ):
        """
Calculates the average value of a function weighted with the Boltzmann distribution.
"""
        raise NotImplementedError

    def variance(
        self,
        func,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
        *args,
        **kwargs,
    ):
        """
Calculates the variance of a function weighted with the Boltzmann distribution.
"""
        raise NotImplementedError


class ThermoMethod(despats.singleton.Singleton):
    """
Decides between different strategies.
"""

    def __init__(self):
        self.__strat = FullCalcStrategy.getsingleton()

    def setstrat(self, strat: ThermoStrategy):
        """
Sets the current strategy.
"""
        self.__strat = strat

    def getstrat(self):
        """
Gets the current strategy.
"""
        return self.__strat

    def partition(
        self,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp=298.15,
        boltzmann=constants.BOLTZMANN_K,
    ):
        """
Calculates the partition function.
"""
        return self.__strat.partition(hamilt, length, temp, boltzmann)

    def average(
        self,
        func,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        *args,
        temp=298.15,
        boltzmann=constants.BOLTZMANN_K,
        **kwargs,
    ):
        """
Calculates the average.
"""
        return self.__strat.average(
            func, hamilt, length, temp, boltzmann, *args, **kwargs
        )

    def variance(
        self,
        func,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        *args,
        temp=298.15,
        boltzmann=constants.BOLTZMANN_K,
        **kwargs,
    ):
        """
Calculates the variance.
"""
        return self.__strat.variance(
            func, hamilt, length, temp, boltzmann, *args, **kwargs
        )

    def energy(
        self,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp=298.15,
        boltzmann=constants.BOLTZMANN_K,
    ):
        """
Calculates the average energy.
"""
        return self.__strat.average(hamilt.energy, hamilt, length, temp, boltzmann)

    def heatcap(
        self,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp=298.15,
        boltzmann=constants.BOLTZMANN_K,
    ):
        """
Calculates the heat capacity.
"""
        return self.__strat.variance(hamilt.energy, hamilt, length, temp, boltzmann) / (
            boltzmann * temp ** 2
        )

    def magneticsus(
        self,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp=298.15,
        boltzmann=constants.BOLTZMANN_K,
    ):
        """
Calculates the magnetic susceptibility.
"""
        return self.__strat.variance(
            lambda sc: sc.magnetization(), hamilt, length, temp, boltzmann
        ) / (boltzmann * temp)


class PlotValsStrategy(
    despats.singleton.Singleton
):  # pylint: disable=too-few-public-methods
    """
Represents the base strategy for computing the values to plot.
"""

    def calc_plot_vals(self, hamilt: hamiltonian.Hamiltonian, length, temps, boltzmann):
        """
Returns the energies, heat capacities, and magnetic susceptibilities at several
temperatures.
"""
        raise NotImplementedError


class SequentialStrategy(PlotValsStrategy):  # pylint: disable=too-few-public-methods
    """
Calculates the plotting values sequentially.
"""

    def calc_plot_vals(self, hamilt: hamiltonian.Hamiltonian, length, temps, boltzmann):
        """
Returns the energies, heat capacities, and magnetic susceptibilities at several
temperatures.
"""
        return (
            list(
                map(
                    lambda t: ThermoMethod.getsingleton().energy(
                        hamilt, length, t, boltzmann
                    ),
                    temps,
                )
            ),
            list(
                map(
                    lambda t: ThermoMethod.getsingleton().heatcap(
                        hamilt, length, t, boltzmann
                    ),
                    temps,
                )
            ),
            list(
                map(
                    lambda t: ThermoMethod.getsingleton().magneticsus(
                        hamilt, length, t, boltzmann
                    ),
                    temps,
                )
            ),
        )


class ThreadedStrategy(PlotValsStrategy):
    """
Calculates the plotting values in several threads.
"""

    def __init__(self):
        super().__init__()
        self._threads = max(32, 4 + os.cpu_count())

    def getthreads(self):
        """
Gets the number of threads.
"""
        return self._threads

    def setthreads(self, threads):
        """
Sets the number of threads.
"""
        self._threads = threads

    def calc_plot_vals(self, hamilt: hamiltonian.Hamiltonian, length, temps, boltzmann):
        """
Returns the energies, heat capacities, and magnetic susceptibilities at several
temperatures.
"""
        exc = concurrent.futures.ThreadPoolExecutor(self.getthreads())
        out = (
            list(
                exc.map(
                    lambda t: ThermoMethod.getsingleton().energy(
                        hamilt, length, t, boltzmann
                    ),
                    temps,
                )
            ),
            list(
                exc.map(
                    lambda t: ThermoMethod.getsingleton().heatcap(
                        hamilt, length, t, boltzmann
                    ),
                    temps,
                )
            ),
            list(
                exc.map(
                    lambda t: ThermoMethod.getsingleton().magneticsus(
                        hamilt, length, t, boltzmann
                    ),
                    temps,
                )
            ),
        )
        exc.shutdown()
        return out


class PlotValsMethod(despats.singleton.Singleton):
    """
Decides between methods for computing the values for the plotter.
"""

    def __init__(self):
        super().__init__()
        self._strat = ThreadedStrategy.getsingleton()

    def getstrat(self):
        """
Gets the current strategy instance.
"""
        return self._strat

    def setstrat(self, strat):
        """
Sets the current strategy instance.
"""
        self._strat = strat

    def calc_plot_vals(
        self,
        hamilt: hamiltonian.Hamiltonian,
        length,
        temps,
        boltzmann=constants.BOLTZMANN_K,
    ):
        """
Returns the energies, heat capacities, and magnetic susceptibilities at several
temperatures.
"""
        return self._strat.calc_plot_vals(hamilt, length, temps, boltzmann)


class FullCalcStrategy(ThermoStrategy):
    """
Calculates values using every configuration in python.
"""

    def partition(
        self,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
    ):
        """
Returns the value of the partition function for a Hamiltonian at a given
temperature and a boltzmann constant with given units.
"""
        return sum(
            math.exp(-hamilt.energy(spins.SpinInteger(sp, length)) / (boltzmann * temp))
            for sp in range(2 ** length)
        )

    def average(
        self,
        func,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
        *args,
        **kwargs,
    ):
        """
Find the value of an intrinsic property normalized by the partition function.
"""

        return sum(
            func(spins.SpinInteger(sp, length), *args, *kwargs)
            * math.exp(
                -hamilt.energy(spins.SpinInteger(sp, length)) / (boltzmann * temp)
            )
            for sp in range(2 ** length)
        ) / self.partition(hamilt, length, temp, boltzmann)

    def variance(
        self,
        func,
        hamilt: hamiltonian.Hamiltonian,
        length: int,
        temp: float,
        boltzmann: float,
        *args,
        **kwargs,
    ):
        """
Find the variance of an intrinsic property normalized by the partition function.
"""
        part = self.partition(hamilt, length, temp, boltzmann)
        head = (
            sum(
                func(spins.SpinInteger(sp, length), *args, **kwargs) ** 2
                * math.exp(
                    -hamilt.energy(spins.SpinInteger(sp, length)) / (boltzmann * temp)
                )
                for sp in range(2 ** length)
            )
            / part
        )
        tail = (
            sum(
                func(spins.SpinInteger(sp, length), *args, **kwargs)
                * math.exp(
                    -hamilt.energy(spins.SpinInteger(sp, length)) / (boltzmann * temp)
                )
                for sp in range(2 ** length)
            )
            ** 2
            / part ** 2
        )
        out = head - tail
        if out < 0:
            raise ArithmeticError(
                f"Variance ({out} = {head} - {tail}) was less than 0!"
            )
        return out
