Installation
============

If you don't want to install the special C backend, you can skip this.
First, you need to tell Make where to find ``Python.h``. For Linux systems, this can be found under ``/usr/include/python3.x``, replacing ``x`` with your python version. The default value for this is ``/usr/include/python3.6``, since that is how it is set up on my machine. After that, there is nothing else to do. The command to do this is

.. code-block:: bash

   $ export PYHEADER=/path/to/headers; make all

The definition for this macro is in ``ising/src/defs.mk``, where its default value can be edited directly.
