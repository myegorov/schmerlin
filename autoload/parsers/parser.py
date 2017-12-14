import os
from errno import ENOENT

class Parser:
    def __init__(self, fpath, dup):
        """ Receives path to keywords file and DUP flag.
        """
        self.DUP = dup
        if not os.path.exists(fpath):
            raise FileNotFoundError(ENOENT, os.strerror(ENOENT), fpath)
        self.fpath = fpath

