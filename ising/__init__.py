"""Ising package"""

# Add imports here
from .constants import *
from .hamiltonian import *
from .spins import *
from .thermo import *
from .fastcwrapper import *

try :
    from .fastc import *
except Exception :
    pass

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions



