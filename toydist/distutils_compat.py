import argparse
import os
import os.path
import sys

from .core import PackageDescription
from .package_info import PackageInfo
from .utils import makedirs


def egg_info_cmd(ns):
    package = PackageDescription.from_yaml("setup.yaml")

    egg_info_builder = EggInfoBuilder(package)
    egg_info_builder.create()


def parse_argv(argv):
    p = argparse.ArgumentParser()
    subparsers = p.add_subparsers()

    egg_info_p = subparsers.add_parser("egg_info")
    egg_info_p.set_defaults(func=egg_info_cmd)

    args = p.parse_args(argv)
    args.func(args)


def setup(argv=None):
    argv = argv or sys.argv[1:]
    parse_argv(argv)


class EggInfoBuilder(object):
    def __init__(self, package):
        self.package = package

    def create(self):
        makedirs(self.egg_info_directory)
        self._create_top_level()
        self._create_pkg_info()

    @property
    def egg_info_directory(self):
        return self.package.name + ".egg-info"

    @property
    def _top_level(self):
        top_level_names = set(
            p.split(".", 1)[0] for p in self.package.distribution_names
        )
        return "\n".join(sorted(top_level_names))

    def _create_top_level(self):
        filename = os.path.join(self.egg_info_directory, "top_level.txt")
        with open(filename, "wt") as fp:
            fp.write(self._top_level)

    def _create_pkg_info(self):
        pkg_info = PackageInfo.from_package(self.package)

        filename = os.path.join(self.egg_info_directory, "PKG-INFO")
        with open(filename, "wt") as fp:
            fp.write(pkg_info.to_string())
