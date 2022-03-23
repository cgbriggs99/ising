Hamiltonian
===========

.. py:module:: ising.hamiltonian

Contains definitions for Hamiltonians for the Ising problem.

.. py:class:: Hamiltonian(coupling, magnet)

   Represents a Hamiltonian for an Ising system.

   :canonical: ising.hamiltonian.Hamiltonian
   :param float coupling: The spin coupling constant for the system.
   :param float magnet: The strength of the magnetic field in the direction of the spins.

   .. py:method:: getcoupling()

      Gets the coupling constant stored in the Hamiltonian.

      :return: The value of the coupling constant.
	       
   .. py:method:: getmagnet()

      Gets the strength of the magnetic field stored in the Hamiltonian.

      :return: The strength of the magnetic field.

   .. py:method:: setcoupling(value)

      Sets the value of the coupling constant.

      :param float value: The new value of the coupling constant.
      :return: The new value of the coupling constant.

   .. py:method:: setmagnet(value)

      Sets the strength of the magnetic field.

      :param float value: The new strength of the magnetic field.
      :return: The new strength of the magnetic field.

   .. py:method:: energy(spin)

      Finds the energy of a spin configuration with the parameters specified by the Hamiltonian. Uses the equation

      .. math::

	 E = J\sum_{\left\langle i,j\right\rangle} S_i S_j + M \sum_i S_i

      :param spin: The spin configuration.
      :type spin: :py:class:`ising.spins.SpinConfig`
      :return: The energy of the given spin configuration.

   .. py:method:: temperature(spin, [boltzmann = BOLTZMANN_K])

      Finds the energy divided by the Boltzmann constant.

      :param spin: The spin configuration.
      :type spin: :py:class:`ising.spins.SpinConfig`
      :param float boltzmann: Value of the Bolztmann constant to use. Defaults to :py:data:`ising.constants.BOLTZMANN_K`.
      :return: The energy of the spin configuration divided by the Boltzmann constant.
      
