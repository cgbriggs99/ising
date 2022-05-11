Main Module Documentation
=========================

This module contains the code needed to run as a command line program.

.. py:module:: ising.__main__

.. py:function:: main([pass_args = None, test = False])

   Run the plotting function. If ``test == True``, then the plots will not be shown.

   :param pass_args: A list of strings represent the arguments to pass to the command line parser. See :program:`ising` for a list of available command options. When ``pass_args == None``, the options are taken from the command line invocation. An example would be ``main(pass_args = ["--length", "5", "--python"])`` which would set the number of particles to 5 and use the python backend. Defaults to ``None``, which will pull options from the command line.
   :type pass_args: list(str)
   :param bool test: Whether this is invoked as a test. Does not produce plots. Defaults to ``False``, which will produce plots.
