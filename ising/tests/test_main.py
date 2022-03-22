#!/usr/bin/python3

import pytest
import ising

def test_main() :
    assert(all(map(lambda x : x is not None, ising.main(test = True))))
    assert(all(map(lambda x : x is not None, ising.main(pass_args = ["--python"],
                                                        test = True))))
    
