import os.path
import sys

from distutils.command.sdist import sdist as old_sdist


class sdist(old_sdist):
    def add_defaults(self):
        old_sdist.add_defaults(self)

        if os.path.exists("setup.yaml"):
            self.filelist.append("setup.yaml")
