# TODO: harden

import os
import textwrap as tw
from errno import ENOENT

class Parser:
    # config
    IDEPATH = '.ide' # subdirectory to look for <fname>.basis
    BASIS_EXT = '.basis' # flat basis file extension
    SYM = {
        'type': u"\u03C4",
        'datatype': u"\u03B4",
        'eqtype': u"\u2261",
        'con': u"\u039A",
        'val': u"\u03B1",
        'exception': u"\u26A1",
        'signature': '',
        'structure': '',
        'functor': ''
    }

    def __init__(self, fpath):
        self.basis_file = os.path.normpath(os.path.join(
                os.path.dirname(fpath),
                self.IDEPATH,
                os.path.basename(fpath) + self.BASIS_EXT))
        if not os.path.exists(self.basis_file):
            raise FileNotFoundError(ENOENT, os.strerror(ENOENT), self.basis_file)

    def parse(self):
        with open(self.basis_file, 'r') as infile:
            res = []
            state = None # current state
            for line in infile:
                # print('processing line:', line)
                if line.startswith('type'):
                    state = 'type'
                    res.append(self.wrap(*self._type(line, state)))
                elif line.startswith('datatype'):
                    state = 'datatype'
                    res.append(self.wrap(*self._type(line,state)))
                elif line.startswith('con'):
                    state = 'con'
                    res.append(self.wrap(*self._ident(line, state)))
                elif line.startswith('val'):
                    state = 'val'
                    res.append(self.wrap(*self._ident(line, state)))
                elif line.startswith('exception'):
                    state = 'exception'
                    res.append(self.wrap(*self._exn(line, state)))
                else: # basis
                    continue

            return res

    def wrap(self, word, kind, menu, info):
        if info is not None:
            return {'word': word,
                    'kind': '[%s]' %self.SYM[kind],
                    'menu': menu,
                    'info': info}
        else:
            return {'word': word,
                    'kind': '[%s]' %self.SYM[kind],
                    'menu': menu}

    def _type(self, line, state):
        parts = line.split(' = ')
        word = parts[0].strip().split()[-1]
        return (word, state, parts[0], line.strip())

    def _ident(self, line, state):
        identifier = line[len(state):].strip().split()[0]

        # check if symbolic
        if identifier[0].isalnum() or identifier[0] == "'":
            return (identifier[:-1], state, line[:len(state) + len(identifier)], line.strip())
        else:
            return (identifier, state, line[:len(state) + 1 + len(identifier)], line.strip())

    def _exn(self, line, state):
        return (line[len(state):].strip(), state, line.strip(), None)

if __name__ == "__main__":
    fpath = '/home/max/projects/schmerlin/autoload/example.smlb'
    parser = Parser(fpath)
    print(parser.parse())
