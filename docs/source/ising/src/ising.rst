Ising C Worker Functions
========================

The actual worker for the C backend. Prototypes can be found in ``ising.h``.

.. c:type:: pass_args_t

   Contains the data to pass to each thread.

   .. c:var:: int index

      The index of the worker thread that is working on this set of values.

   .. c:var:: int threads

      The total number of threads.

   .. c:var:: int positions

      The number of positions in the Ising model.

   .. c:var:: int len

      The number of temperatures.

   .. c:var:: double coupling

      Value of the spin coupling constant.

   .. c:var:: double magnet

      Value of the magnetic coupling constant.

   .. c:var:: double boltzmann

      Value of the Boltzmann constant.

   .. c:var:: const double *temps

      List of temperatures to calculate at.

   .. c:var:: double *out_ens

      Array of energies. Acts as the output for :c:func:`compute_vals`.

   .. c:var:: double *out_heat

      Array of heat capacities. Acts as the output for :c:func:`compute_vals`.

   .. c:var:: double *out_magsus

      Array of magnetic susceptibilities. Acts as the output for :c:func:`compute_vals`.

.. c:type:: struct bitvec_32_t
	      
   Splits a 32 bit value into 8 bit chunks. Interactions with a packed bit-field struct should be optimized at compile time.

   .. c:var:: uint8_t a, b, c, d

.. c:type:: union conv_t

   Converts between an unsigned 32 bit value (``uint32_t``) and a ``bitvec_32_t``.

   .. c:var:: uint32_t in

   .. c:var:: bitvec_32_t vec

   
.. c:function:: static inline int bitcount(uint32_t in)

   Count the number of one bits.

   :param in: The value to count the bits of.
   :type in: uint32_t
   :return: The number of one bits in the number.

.. c:macro:: MAGNETIZATION(I, L)

   Computes the magnetization part of the energy. First, it finds the number of one bits. Then, multiplies by two, and subtracts the total number of positions. This is done using bit arithmetic to make it blazing fast.

   :param I: The number representing the state.
   :param L: The number of positions in the Ising model.
   :return: The magnetization part, not multiplied by the coupling constant.

.. c:macro:: SPINCOUPLE(I, L)

   Computes the spin coupling part of the energy. First, it shifts the number to mimic a rotation. Then, it uses a bitwise XOR to perform multiplications between +1 and -1. Then, it computes the number of one bits, multiplies by two, and subtracts the number of positions.

   :param I: The number representing the state.
   :param L: The number of positions in the Ising model.
   :return: The spin coupling part, not multiplied by the coupling constant.

.. c:function:: static void *compute_vals(void *arg)

   Worker function to be passed to the threads.

   :param arg: The arguments. Defined in the function as :c:type:`void *`, but treated as :c:type:`pass_args_t *`.
   :type arg: void *
   :return: NULL. All outputs are placed in :c:type:`pass_args_t`.


.. c:function:: int threaded_ising(int positions, double coupling, double magnet, double boltzmann, const double *temps, int len_temps, double *out_ens, double *out_heat, double *mag_sus, int threads)

   Master function for the threads. Dispatches the workers with the appropriate indices so that they can chop up the work correctly, then runs on the data itself.

   :param int positions: The number of positions in the Ising model.
   :param double coupling: The spin coupling constant.
   :param double magnet: The magnet coupling constant.
   :param temps: The list of temperatures.
   :type temps: const double \*
   :param int len_temps: The length of the list of temperatures.
   :param out_ens: The ouptut array that will contain the energies.
   :type out_ens: double \*
   :param out_heat: The output array that will contain the heat capacities.
   :type out_heat: double \*
   :param mag_sus: The output array that will contain the magnetic susceptibilities.
   :type mag_sus: double \*
   :param int threads: The number of threads to run, including the master.
   :return: 0 on success.
