Thermodynamics
==============

Contains functions for computing thermodynamic data.

.. py:module:: ising.thermo

.. py:class:: ThermoStrategy

   Represents a strategy for calculating the thermodynamic properties. It is an abstract method that implements :py:class:`ising.despats.singleton.Singleton`.

   .. py:method:: partition(hamilt, length, temp, boltzmann)

      Finds the partition function.

      :abstractmethod:
      :param hamilt: The :py:class:`ising.hamiltonian.Hamiltonian` object to pull properties from.
      :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
      :param int length: The number of positions in the Ising configuration.
      :param float temp: The temperature to run this compuation at.
      :param float boltzmann: The value of the Boltzmann constant to use.
      :return: The value of the partition function.

   .. py:method:: average(func, hamilt, length, temp, boltzmann, \*args, \*\*kwargs)

      Finds the expectation value of a function weighted by the Boltzmann distribution.

      :abstractmethod:
      :param func: The function to average. ``*args`` and ``**kwargs`` are passed to this function directly.
      :type func: func(spins: :py:class:`ising.spins.SpinConfig`, \*args, \*\*kwargs)
      :param hamilt: The Hamiltonian to pull properties from.
      :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
      :param int length: The number of positions in the Ising system.
      :param float temp: The temperature to run the computation at.
      :param float boltzmann: The value of the Boltzmann constant. 
      :return: The average value of the function.

   .. py:method:: variance(func, hamilt, length, temp, boltzmann, \*args, \*\*kwargs)
      Finds the variance of a function weighted by the Boltzmann distribution.

      :abstractmethod:
      :param func: The function to average. ``*args`` and ``**kwargs`` are passed to this function directly.
      :type func: func(spins: :py:class:`ising.spins.SpinConfig`, \*args, \*\*kwargs)
      :param hamilt: The Hamiltonian to pull properties from.
      :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
      :param int length: The number of positions in the Ising system.
      :param float temp: The temperature to run the computation at.
      :param float boltzmann: The value of the Boltzmann constant. 
      :return: The variance of the function.

.. py:class:: ThermoMethod

   Holds the current method for calculating thermodynamic properties. Initialized to :py:class:`ising.thermo.FullCalcsStrategy`.

   .. py:method:: setstrat(strat)

      Sets the strategy to use.

      :param strat: The strategy instance to use.
      :type strat: :py:class:`ising.thermo.ThermoStrategy`

   .. py:method:: getstrat()

      Gets the current strategy instance.

      :return: The current strategy instance.

   .. py:method:: partition(hamilt, length, temp = 298.15, boltzmann = :py:data:`ising.constants.BOLTZMANN_K`)

      Calculates the partition function using the current strategy.

      :param hamilt: The Hamiltonian object to pull data from.
      :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
      :param int length: The number of positions in the Ising configuration.
      :param float temp: The temperature to calculate at. Defaults to 298.15 K.
      :param float boltzmann: The value of the Boltzmann constant. Defaults to :py:data:`ising.constants.BOLTZMANN_K`.
      :return: The value of the partition function.

   .. py:method:: average(func, hamilt, length, temp = 298.15, boltzmann = :py:data:`ising.constants.BOLTZMANN_K`, \*args, \*\*kwargs)

      Calculates the average value of a function.

      :param func: The function to average. ``\*args`` and ``\*\*kwargs`` are passed directly to this function.
      :type func: func(spin : :py:class:`ising.spins.SpinConfig`, \*args, \*\*kwargs)
      :param hamilt: The Hamiltonian to pull data from.
      :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
      :param int length: The number of positions in the Ising configuration.
      :param float temp: The temperature to calculate at. Defaults to 298.15 K.
      :param float boltzmann: The value of the Boltzmann constant. Defaults to :py:data:`ising.constants.BOLTZMANN_K`.
      :return: The average value of the function.

   .. py:method:: variance(func, hamilt, length, temp = 298.15, boltzmann = :py:data:`ising.constants.BOLTZMANN_K`, \*args, \*\*kwargs)

      Calculates the variance of a function.

      :param func: The function to find the variance of. ``\*args`` and ``\*\*kwargs`` are passed directly to this function.
      :type func: func(spin : :py:class:`ising.spins.SpinConfig`, \*args, \*\*kwargs)
      :param hamilt: The Hamiltonian to pull data from.
      :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
      :param int length: The number of positions in the Ising configuration.
      :param float temp: The temperature to calculate at. Defaults to 298.15 K.
      :param float boltzmann: The value of the Boltzmann constant. Defaults to :py:data:`ising.constants.BOLTZMANN_K`.
      :return: The variance of the function.

.. py:class:: FullCalcStrategy

   An implementation of :py:class:`ising.thermo.ThermoStrategy` that runs for each possible spin configuration.

.. py:class:: PlotValsStrategy

   Represents the base class for different ways to compute the energy, heat capacity, and magnetic susceptibilities at different temperatures.

   .. py:method:: calc_plot_vals(self, hamilt, length, temps, boltzmann)

      Calculates the values.

      :param hamilt: The Hamiltonian to use to calculate the energy.
      :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
      :param int length: The number of positions in the Ising model.
      :param list(float) temps: The temperatures to compute the values at.
      :param float boltzmann: The value of the Boltzmann constant.
      :return: Three lists containing the energies, heat capacities, and magnetic susceptibilities.

.. py:class:: SequentialStrategy

   See :py:class:`ising.thermo.PlotValsStrategy`. Computes the values in a single thread.

.. py:class:: ThreadedStrategy

   See :py:class:`ising.thermo.PlotValsStrategy`. Computes the values in several threads.

   .. py:method:: getthreads(self)

      Gets the number of threads.

      :return: The number of threads to use for the partition function.

   .. py:method:: setthreads(self, threads : int)

      Sets the number of threads.

      :param int threads: The new number of threads.

.. py:class:: PlotValsMethod

   Contains the current method to compute the plotted values.

   .. py:method:: getstrat(self)

      Gets the current strategy instance.

      :return: A reference to the current strategy.

   .. py:method:: setstrat(self, strat)

      Sets the current method to a new method.

      :param strat: A reference to the new strategy.
      :type strat: :py:class:`ising.thermo.PlotValsStrategy`
