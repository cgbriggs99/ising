#!/usr/bin/python3

"""
Test the main module.
"""

import pytest
import ising.__main__

__ARGS = ["--length", "8"]


def test_cback():
    """
Test the C backend.
"""
    assert all(
        map(
            lambda x: x is not None,
            ising.__main__.main(pass_args=__ARGS + ["--backend", "c"], test=True),
        )
    )


def test_mcback():
    """
Test the Monte-Carlo backend.
"""
    assert all(
        map(
            lambda x: x is not None,
            ising.__main__.main(
                pass_args=__ARGS
                + ["--backend", "monte-carlo", "--depth", "10", "--mc-points", "100"],
                test=True,
            ),
        )
    )


def test_fullback():
    """
Test the Python backend.
"""
    assert all(
        map(
            lambda x: x is not None,
            ising.__main__.main(pass_args=__ARGS + ["--backend", "python"], test=True),
        )
    )
