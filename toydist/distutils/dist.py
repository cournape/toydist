from __future__ import absolute_import

from toydist.core import PackageDescription

from .commands.sdist import sdist
from .utils import _is_setuptools_activated


if _is_setuptools_activated():
    from setuptools import Distribution as OldDistribution
else:
    from distutils.dist import Distribution as OldDistribution


_MONKEYED_CLASSES = {"sdist": sdist}


class Distribution(OldDistribution):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}

        attrs = _setup_cmd_classes(attrs)

        self.package = PackageDescription.from_yaml("setup.yaml")

        attrs.update({
            "name": self.package.name,
            "version": str(self.package.version),
            "long_description": self.package.description,
            "description": self.package.summary,
            "packages": self.package.packages,
        })

        OldDistribution.__init__(self, attrs)


def _setup_cmd_classes(attrs):
    cmdclass = attrs.get("cmdclass", {})
    for klass_name, klass in _MONKEYED_CLASSES.items():
        if not klass_name in cmdclass:
            cmdclass[klass_name] = klass
    attrs["cmdclass"] = cmdclass
    return attrs
