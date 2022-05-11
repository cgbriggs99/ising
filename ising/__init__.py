"""Ising package"""

# Add imports here
from .constants import *
from .hamiltonian import *
from .spins import *
from .thermo import *
from .fastc import *
from .fastcwrapper import *
from .despats import *
from .montecarlo import *
from .graph import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
