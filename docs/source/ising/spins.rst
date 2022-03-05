Spins
=====

.. py:module:: ising.spins

   Contains representations for spin configurations.

   :canonical: ising.spins

.. py:class:: SpinConfig

   Represents a general spin configuration.

   :canonical: ising.spins.SpinConfig

   .. py:method:: __len__()

      Gets the number of positions in the spin configuration.

      :raises: NotImplemented

   .. py:method:: __getitem__(index)

      Allows for subscripting.

      :raises: NotImplemented

   .. py:method:: __setitem__(index)

      Allows for assigning to a position.

      :raises: NotImplemented

   .. py:method:: __iter__()

      Allows for iterating over the positions.

      :raises: NotImplemented

   .. py:method:: __str__()

      Returns a string representation using spin-arrow notation to show the spin state.

      :return: A string with up and down arrows.

   .. py:method:: magnetization()

      Returns the spin excess of the configuration. That is, the number of up spins minus the number of down spins.

      :return: The spin excess.

.. py:class:: SpinMatrix(
