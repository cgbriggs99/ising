Thermodynamics
==============

.. py:module:: ising.thermo

Contains functions for computing thermodynamic data.

.. py:function:: partition(hamilt, length, [temp = 298.15, boltzmann = BOLTZMANN_K])

   Find the value of the partition function.

   :param hamilt: :py:class:`ising.hamiltonian.Hamiltonian` object containing the coupling constants.
   :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
   :param int length: The number of positions in the Ising system.
   :param float temp: The temperature to compute the partition function for. Defaults to 298.15 K.
   :param float boltzmann: The value of the Boltzmann constant. Defaults to :py:data:`ising.constants.BOLTZMANN_K`.
   :return: The value of the partition function.

.. py:function:: average_value(func, hamilt, length, [temp = 298.15, boltzmann = BOLTZMANN_K])

   Find the average value of a property, weighted by the Boltzmann parameters.

   :param func: Function that takes a SpinConfig as its first argument.
   :type func: function(:py:class:`ising.spins.SpinConfig`, \*args, \*\*kwargs)
   :param hamilt: :py:class:`ising.hamiltonian.Hamiltonian` object containing the coupling constants.
   :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
   :param int length: The number of positions in the Ising system.
   :param float temp: The temperature to compute the partition function for. Defaults to 298.15 K.
   :param float boltzmann: The value of the Boltzmann constant. Defaults to :py:data:`ising.constants.BOLTZMANN_K`.
   :return: The average value of a property.

.. py:function:: variance(func, hamilt, length, [tmep = 298.15, boltzmann = BOLTZMANN_K])

   Find the variance of a property, weighted by the Boltzmann parameters.

   :param func: Function that takes a :py:class:`ising.spins.SpinConfig` as its first argument.
   :type func: function(:py:class:`ising.spins.SpinConfig`, \*args, \*\*kwargs)
   :param hamilt: :py:class:`ising.hamiltonian.Hamiltonian` object containing the coupling constants.
   :type hamilt: :py:class:`ising.hamiltonian.Hamiltonian`
   :param int length: The number of positions in the Ising system.
   :param float temp: The temperature to compute the partition function for. Defaults to 298.15 K.
   :param float boltzmann: The value of the Boltzmann constant. Defaults to :py:data:`ising.constants.BOLTZMANN_K`.
   :return: The variance of a property.
