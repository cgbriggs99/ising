Hamiltonian
===========

Contains definitions for Hamiltonians for the Ising problem.

.. py:module:: ising.hamiltonian

.. py:class:: Hamiltonian

   Base class for all Hamiltonians.

   .. py:method:: energy(spin)

      Unimplemented energy method.

      :param spin: The spin configuration to find the energy of.
      :type spin: :py:class:`ising.spins.SpinConfig`

   .. py:method:: temperature(spin, boltzmann)

      Finds the normalized energy of a spin configuration with the given Boltzmann constant.

      :param spin: The spin configuration.
      :type spin: :py:class:`ising.spins.SpinConfig`
      :param float boltzmann: The boltzmann constant. Defaults to :py:data:`ising.constants.BOLTZMANN_K`.

.. py:class:: ConstantHamiltonian(coupling, magnet)

   Represents a Hamiltonian for an Ising system with constant spin coupling and magnetic coupling.

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

.. py:class:: PeriodicHamiltonian(coupling, magnet)

   See the constructor for :py:class:`ConstantHamiltonian`. Extends :py:class:`ConstantHamiltonian`. Has periodic boundary conditions.

   .. py:method:: energy(spin)

      Finds the energy of a spin configuration with the parameters specified by the Hamiltonian. Uses the equation

      .. math::

	 E = J\sum_{\left\langle i,j\right\rangle} S_i S_j + M \sum_i S_i

      :param spin: The spin configuration.
      :type spin: :py:class:`ising.spins.SpinConfig`
      :return: The energy of the given spin configuration.

.. py:class:: NPHamiltonian(coupling, magnet)

   See the constructor for :py:class:`ConstantHamiltonian`. Extends :py:class:`ConstantHamiltonian`. Has non-periodic boundary conditions.

   .. py:method:: energy(spin)

      Finds the energy of a spin configuration with the parameters specified by the Hamiltonian.

      :param spin: The spin configuration.
      :type spin: :py:class:`ising.spins.SpinConfig`
      :return: The energy of the given spin configuration.

.. py:class:: GraphHamiltonian(conns, mags)

   Represents a Hamiltonian with arbitrary connections between spins.

   :param conns: A graph representing the connections between spins.
   :type conns: :py:class:`ising.graph.Graph`
   :param mags: The magnetic constants. If it is a single value, it is applied to all. If it is multiple values, it will be applied to each vertex in order.
   :type mags: float or list(float)

   .. py:method:: getconns()

      Returns the graph representing the connections.

      :return: The graph representing the connections between interacting spins.

   .. py:method:: getmagnet()

      Returns the magnetic constant(s).

      :return: The magnetic constant or constants.

   .. py:method:: setmagnet(mags)

      Sets the magnetic constant.

      :param mags: The magnetic constant or constants.
      :type mags: float or list(float)
      :return: The new value.

   .. py:method:: energy(spin)

      Calculates the energy of a given configuration.

      :param spin: The spin configuration.
      :type spin: :py:class:`ising.spins.SpinConfig`.
