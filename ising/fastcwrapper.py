#!/usr/bin/python3

"""
Wraps the C code in Python.
"""

try:
    from . import hamiltonian
    from . import thermo
    from . import spins
except ImportError:
    import hamiltonian
    import thermo
    import spins

import os


class CThermoStrategy(thermo.ThermoStrategy):
    """
Calculates values in C. Only partition function is threaded.
"""

    def __init__(self):
        super().__init__()
        self._threads = max(32, 4 + os.cpu_count())

    def getthreads(self):
        """
Gets the number of threads.
"""
        return self._threads

    def setthreads(self, threads : int):
        """
Sets the number of threads.
"""
        self._threads = threads

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
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian):
            return fastc.p_partition(
                length,
                hamilt.getcoupling(),
                hamilt.getmagnet(),
                temp,
                boltzmann,
                self.getthreads(),
            )
        return thermo.FullCalcStrategy.getsingleton().partition(
            hamilt, length, temp, boltzmann
        )

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
Calculates the average.
"""
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian):
            return fastc.p_average(
                lambda sp: func(spins.SpinInteger(sp, length)),
                length,
                hamilt.getcoupling(),
                hamilt.getmagnet(),
                temp,
                boltzmann,
            )
        return thermo.FullCalcStrategy.getsingleton().average(
            func, hamilt, length, temp, boltzmann, *args, **kwargs
        )

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
Calculates the variance.
"""
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian):
            return fastc.p_variance(
                lambda sp: func(spins.SpinInteger(sp, length)),
                length,
                hamilt.getcoupling(),
                hamilt.getmagnet(),
                temp,
                boltzmann,
            )
        return thermo.FullCalcStrategy.getsingleton().variance(
            func, hamilt, length, temp, boltzmann, *args, **kwargs
        )


class CPlotStrategy(thermo.PlotValsStrategy):
    """
Calculates the values for the plotter in C. Very parallelized.
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
        if isinstance(hamilt, hamiltonian.PeriodicHamiltonian):
            return fastc.p_plots(
                length,
                hamilt.getcoupling(),
                hamilt.getmagnet(),
                list(temps),
                boltzmann,
                self.getthreads(),
            )
        return super().calc_plot_vals(hamilt, length, temps, boltzmann)


try:
    from . import fastc
except ImportError:
    import fastc
