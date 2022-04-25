Singleton
=========

Implementation of the singleton pattern.

.. py:module:: ising.despats.singleton

.. py:class:: Singleton

   Base class for singletons.

   .. py:attribute:: __singeltonptr

      The sole pointer to the singleton.

   .. py:classmethod:: getsingleton()

      Returns the singleton instance if it exists. If it does not exist, create it and return it.

      :return: The singleton instance.
