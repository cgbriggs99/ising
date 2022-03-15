"""Ising package"""

# Add imports here
from .ising import *
from .hamiltonian import *
from .spins import *
from .thermo import *

# This module is not guaranteed.
try :
    from .src.fafb import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions



