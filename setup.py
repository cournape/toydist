import os

if os.environ.get("TOYDIST_USE_DISTUTILS"):
    # Internally use distutils
    import setuptools
    from toydist.distutils import monkey_patch, setup
    monkey_patch()
    setup()
else:
    # Don't use distutils at all
    from toydist.distutils_compat import setup
    setup()
