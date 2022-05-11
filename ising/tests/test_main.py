#!/usr/bin/python3

import pytest
import ising.__main__

__other_args = ["--length", "8"]

def test_cback() :
    assert(all(map(lambda x : x is not None,
                   ising.__main__.main(pass_args = __other_args +
                                       ["--backend", "c"], test = True))))
def test_mcback() :
    assert(all(map(lambda x : x is not None,
                   ising.__main__.main(pass_args = __other_args +
                                       ["--backend", "monte-carlo",
                                        "--depth", "10",
                                        "--mc-points", "100"],
                                                        test = True))))
def test_fullback() :
    assert(all(map(lambda x : x is not None,
                   ising.__main__.main(pass_args = __other_args +
                                       ["--backend", "python"],
                                                        test = True))))
    
