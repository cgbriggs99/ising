#!/usr/bin/python3

import numpy as np
import math

import .spins
import .hamiltonian

"""
Computes properties of Ising systems.
"""

boltzmann_k = 1.38064852e-23 # J/K


if __name__ == "__main__":
    import matplotlib.pyplot as plot
