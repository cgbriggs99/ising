"""
Unit and regression test for the ising package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import ising


def test_ising_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "ising" in sys.modules
