Monte-Carlo Algorithm
=====================

Contains computations for the Monte-Carlo algorithm and Metropolis sampling.

.. py:module:: ising.montecarlo

.. py:class:: RandomIterator(start_end, [stop, [step]])

   An iterator of random integers between start (inclusive) and stop (exclusive), separated by a step. It can be used with the ``in`` keyword, as well as :py:func:`next` and :py:func:`iter`.

   :param start_end: If a second argument is passed, this represents the lower bound. If only one argument is passed, the lower bound is assumed to be zero, and this represents the upper bound. Used like :py:class:`range`.
   :param stop: If this is passed, it represents the upper bound.
   :param step: If this is passed, it represents the step size between members. Otherwise, the step is set to 1.


.. py:class:: MonteCarloStrategy

   Implementation of :py:class:`ising.thermo.ThermoStrategy` that selects several random states and uses those to approximate properties.

   .. py:method:: setpoints(points : int)

      Sets the number of points to pick.

      :param int points: The number of points to pick.

   .. py:method:: getpoints()

      Gets the number of points being picked.

      :return: The number of points being picked.

.. py:class:: MetropolisStrategy

   Implementation of :py:class:`ising.thermo.ThermoStrategy` that uses Metropolis sampling instead of simply picking random states. Defaults to 1000 points, following 10 steps for each point.

   .. py:method:: setdepth(depth : int)

      Sets the length of a chain before it is stopped being followed.

      :param int depth: The maximum depth of a chain.

   .. py:method:: getdepth()

      Gets the length of a chain before it is stopped.

      :return: The maximum depth of a chain.

   .. py:method:: setpoints(points : int)

      Sets the number of points to pick.

      :param int points: The number of points to pick.

   .. py:method:: getpoints()

      Gets the number of points being picked.

      :return: The number of points being picked.
