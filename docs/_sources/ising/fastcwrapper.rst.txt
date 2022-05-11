FastC Wrapper
=============

Wraps the :py:func:`plot_vals` function to allow for more customization.

.. py:module:: ising.fastcwrapper

.. py:class:: CThermoStrategy

   See :py:class:`ising.thermo.ThermoStrategy`. Wraps the C backend.

   .. py:method:: getthreads(self)

      Gets the number of threads.

      :return: The number of threads to use for the partition function.

   .. py:method:: setthreads(self, threads : int)

      Sets the number of threads.

      :param int threads: The new number of threads.

.. py:class:: CPlotStrategy

   See :py:class:`ising.thermo.PlotValsStrategy`. Wraps the C backend.

   .. py:method:: getthreads(self)

      Gets the number of threads.

      :return: The number of threads to use for the partition function.

   .. py:method:: setthreads(self, threads : int)

      Sets the number of threads.

      :param int threads: The new number of threads.
