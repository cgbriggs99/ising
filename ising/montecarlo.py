#!/usr/bin/python3


import random
import math
import numpy as np

try :
    from . import spins
except ImportError :
    import spins

def montepoint_intrange(count, start, end = None, step = 1) :
    if end is None :
        start, end = 0, start
    for i in range(count) :
        yield(random.randrange(start, end, step))
    raise StopIteration
    

def montesum(func, coverage, length, *args, **kwargs) :
    """
Returns a sum with Monte-Carlo evaluation.
"""
    numvals = 0
    if 0 <= coverage and coverage <= 1 and type(coverage) is float :
        # If coverage is a percent.
        numvals = int(coverage * 2 ** length)
    else if type(coverage) is int :
        # If coverage is a number of values.
        numvals = coverage
    return sum(func(spins.SpinInteger(sp, length), *args, **kwargs)
               for sp in montepoint_intrange(numvals, 2 ** length))



def partition(coverage, hamilt, length, temp = 298.15,
              boltzmann = ising.BOLTZMANN_K) :
    return montesum(
