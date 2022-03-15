Spins
=====

.. py:module:: ising.spins

Contains representations for spin configurations.
	       
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

.. py:class:: SpinMatrix(data : list(int)) : :py:class:`SpinConfig`

   Represents a spin configuration set up with an array of 1's and -1's representing up and down spins. Implements all the base methods.

      :param data: A list of 1's and -1's.
      :type data: list(int)

.. py:class:: SpinInteger(numeral : int, length : int) : :py:class:`SpinConfig`
	      
   Represents a spin configuration determined from the binary representation of an integer.

   .. py:method:: __iter__()

      :return: A :py:class:`_SpinIntegerIterator` that represents the object.

   .. py:method:: copy()

      :return: A copy of this object.

.. py:class:: _SpinIntegerIterator(other : :py:class:`SpinInteger`)

   Iterator class for :py:class:`SpinInteger`.

   :param other: The :py:class:`SpinInteger` object to iterate over.

