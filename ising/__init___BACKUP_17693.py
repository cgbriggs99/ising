"""Ising package"""

# Add imports here
from .constants import *
from .hamiltonian import *
from .spins import *
from .thermo import *
<<<<<<< HEAD
=======
from .fastcwrapper import *
>>>>>>> da56f9cd41c9923711c628128325629f9ca676c5
from .despats import *

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



