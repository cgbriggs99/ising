Fast C Backend
==============

.. py:module:: ising.src.fastc

C backend that computes the energies, magnetic susceptibilities, and heat capacities faster than Python could ever wish.

.. py:function:: plot_vals(positions, coupling, magnet, temps, boltzmann, threads)

   Calculate the values to plot.

   :param int positions: The number of slots in the Ising model.
   :param float coupling: The coupling constant to use.
   :param float magnet: The magnetic constant to use.
   :param list(float) temps: A list of temperature points for the plots.
   :param float boltzmann: The Bolzmann constant.
   :param int threads: The number of threads to use.
   :return tuple(list(float), list(float), list(float): Three lists, the first being the energies, the second the heat capacities, and the third the magnetic susceptibilities.

   :canonical: ising/src/fastcmodule.c:fastc_pass_to_c

.. c:function:: PyMODINIT_FUNC PyInit_fastc(void)

   Makes the module work.
   
