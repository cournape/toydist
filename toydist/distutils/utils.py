import sys


def _is_setuptools_activated():
    """Returns True if setuptools has already been imported."""
    return "setuptools" in sys.modules
