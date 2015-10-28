import sys


def monkey_patch():
    # keep the import here to avoid any side-effects from mere import of
    # toydist.distutils
    from .dist import Distribution
    from .utils import _is_setuptools_activated

    # Install it throughout the distutils
    _MODULES = []
    if _is_setuptools_activated():
        import setuptools.dist
        _MODULES.append(setuptools.dist)
    import distutils.dist, distutils.core, distutils.cmd
    _MODULES.extend([distutils.dist, distutils.core, distutils.cmd])
    for module in _MODULES:
        if hasattr(module, "Distribution"):
            module._old_Distribution = module.Distribution
            module.Distribution = Distribution


def setup(mode=None):
    """Call setup after monkey-patching with the given mode.

    Parameters
    ----------
    mode: None/str
        'distutils' or 'setuptools' for now
    """
    if mode is None:
        if "setuptools" in sys.modules:
            mode = "setuptools"
        else:
            mode = "distutils"
    if not mode in ("distutils", "setuptools"):
        raise ValueError("Only 'setuptools' and 'distutils' are supported modes")
    __import__(mode)
    monkey_patch()
    from distutils.core import setup as _setup
    return _setup()
