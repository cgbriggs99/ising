#!/usr/bin/python3

import pytest
import ising.__main__

__other_args = ["--length", "8"]

def test_main() :
    assert(all(map(lambda x : x is not None,
                   ising.__main__.main(pass_args = __other_args, test = True))))
    assert(all(map(lambda x : x is not None,
                   ising.__main__.main(pass_args = __other_args + ["--python"],
                                                        test = True))))
    
