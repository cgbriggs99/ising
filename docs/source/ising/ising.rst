Ising
=====
.. py:module:: ising.ising

This module contains the Boltzmann constant and a wrapper for the actual plotting function.
   
.. py:data:: BOLTZMANN_K

   The Boltzmann constant in Joules per Kelvin.

   :type: float
   :value: 1.38064852e-23
   :canonical: ising.ising.BOLTZMANN_K

.. py:function:: fastcwrapper(ham : :py:class:`ising.Hamiltonian`, length : int, temps : iterable, boltzmann = :py:data:`BOLTZMANN_K` : float, threads = ``max(32, 4 + os.cpu_count()`` : int, no_c = False : bool)

   This is a wrapper around :py:func:`ising.src.fastc.plot_vals` which converts iterables to lists, hamiltonians to their parameters, and adds default values for threads, the Boltzmann constant, and contains a flag for whether to actually use the C backend. It also handles whether the C backend is included.

   :param ham: The hamiltonian.
   :type ham: :py:class:`ising.Hamiltonian`
   :param int length: The number of positions in the Ising model.
   :param iterable temps: The temperatures to plot for.
   :param float boltzmann: The Boltzmann constant.
   :param int threads: The number of threads to use.
   :param bool no_c: Whether or not to use the C backend.
