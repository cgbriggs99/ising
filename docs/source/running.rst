Running Ising
=============

To run the Ising application, simply type ``~$ ising`` or ``~$ python ising``. This can be used with a variety of command line options.

.. program:: ising

Compute graphs for an Ising system with periodic boundary conditions.

.. option:: --length N, -l N

Specifies the number of spin particles in the model. Default 10.

.. option:: --coupling X, -j X

Specifies the spin coupling constant. Default -1 * :py:data:`ising.constants.BOLTZMANN_K`.

.. option:: --magnet X, -m X

Specifies the magnetic coupling constant. Default 0.1 * :py:data:`ising.constants.BOLTZMANN_K`.

.. option:: --low-temp X

Specifies the minimum temperature in Kelvin for the graph. Can not be less than or equal to zero. Default 0.1.

.. option:: --high-temp X

Specifies the maximum temperature in Kelvin for the graph. Can not be less than or equal to zero, and should be greater than the minimum. Default 298.15.

.. option:: --boltzmann X, -k X

The value to use as the Boltzmann constant in whatever units needed. Default :py:data:`ising.constants.BOLTZMANN_K`, which is in Joules per Kelvin.

.. option:: --points N, -n N

The number of points to plot. Default 100.

.. option:: --python

Use a Python backend, which is slower. Defaults to using the C backend.
