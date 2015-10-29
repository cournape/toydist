import errno
import os


def makedirs(p):
    try:
        os.makedirs(p)
    except OSError as exc:
        if exc.errno != errno.ENOENT:
            raise
