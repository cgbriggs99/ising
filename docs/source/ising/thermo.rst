Thermodynamics
==============

.. py:module:: ising.thermo

Contains functions for computing thermodynamic data.

.. py:function:: partition

   Find the value of the partition function.

   :param hamilt: Hamiltonian object containing the coupling constants.
   :type hamilt: ising.hamiltonian.Hamiltonian
   :param int length: The number of positions in the Ising system.
   :param float temp: The temperature to compute the partition function for.
   :param float boltzmann: The value of the Boltzmann constant.
   :return: The value of the partition function.

.. py:function:: average_value

   Find the average value of a property, weighted by the Boltzmann parameters.

   :param func: Function that takes a SpinConfig as its first argument.
   :type func: function(SpinConfig, \*args, \*\*kwargs)
   :param hamilt: Hamiltonian object containing the coupling constants.
   :type hamilt: ising.hamiltonian.Hamiltonian
   :param int length: The number of positions in the Ising system.
   :param float temp: The temperature to compute the partition function for.
   :param float boltzmann: The value of the Boltzmann constant.
   :return: The average value of a property.

.. py:function:: variance

   Find the variance of a property, weighted by the Boltzmann parameters.

   :param func: Function that takes a SpinConfig as its first argument.
   :type func: function(SpinConfig, \*args, \*\*kwargs)
   :param hamilt: Hamiltonian object containing the coupling constants.
   :type hamilt: ising.hamiltonian.Hamiltonian
   :param int length: The number of positions in the Ising system.
   :param float temp: The temperature to compute the partition function for.
   :param float boltzmann: The value of the Boltzmann constant.
   :return: The variance of a property.
