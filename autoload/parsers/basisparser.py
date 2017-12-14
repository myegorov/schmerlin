import re
from .parser import Parser

class BasisParser(Parser):
    SYM = {
        'type': u"\u03C4", # tau
        'datatype': u"\u03B4", # delta
        'con': u"\u039A", # Kappa
        'val': u"\u03B1", # alpha
        'exception': u"\u26A1", # high voltage char
        'signature': u"\u03C2", # sigma
        'structure': u"\u2302", # structure
        'functor': u"\u03A6" # Phi
    }


    def __init__(self, fpath, dup):
        super(BasisParser, self).__init__(fpath, dup)
        self.res = []
        self.infile = None # iterator over input basis file
        self.FUNS = {
            'type': self._type,
            'datatype': self._type,
            'con': self._ident,
            'val': self._ident,
            'exception': self._exn,
            'signature': self._sig,
            'structure': self._struct,
            'functor': self._funct
        }


    def parse(self):
        with open(self.fpath, 'r') as infile:
            self.infile = infile
            self.start(None)
            return self.res

    def wrap(self, word, kind, menu, info=''):
        return {'word': word,
                'kind': '[%s]' %self.SYM[kind],
                'menu': menu,
                'info': info,
                'dup': self.DUP}

    def start(self, state=None, **kw):
        line = self.infile.readline()
        while line:
            match = re.search(r'^[a-zA-Z]+', line)
            if match is not None and match.group(0) in self.FUNS:
                # wrap up previous state
                if state is not None: # not done yet
                    self.res.append(self.wrap(
                        kw['word'],
                        state,
                        kw['menu'],
                        ''.join(kw['info'])))
                    kw = {} # reset

                state = match.group(0)
                state, kw = self.FUNS[state](line, state, **kw)
            elif re.match(r'[ \t]', line) is not None: # starts with whitespace
                kw['info'].append(line)
            else: # basis or some unrecognized keyword
                pass

            line = self.infile.readline()

        # reached EOF
        if state is not None: # not done yet
            self.res.append(self.wrap(
                kw['word'],
                state,
                kw['menu'],
                ''.join(kw['info'])))


    def _type(self, line, state, **kw):
        parts = line.split(' = ')
        d = {'word': parts[0].strip().split()[-1],
             'menu': parts[0].strip(),
             'info': [line]}
        return (state, d)

    def _sig(self, line, state, **kw):
        parts = line.strip().split()
        d = {'word': parts[1].strip(),
             'menu': ' '.join(parts[:2]),
             'info': [line]}
        return (state, d)

    def _exn(self, line, state, **kw):
        d = {'word': line[len(state):].strip(),
             'menu': line.strip(),
             'info': [' ']}
        return (state, d)

    def _funct(self, line, state, **kw):
        identifier = line.strip().split()[1]
        d = {'word': identifier,
             'menu': 'functor %s' %identifier,
             'info': [line]
            }
        return (state, d)

    def _ident(self, line, state, **kw):
        identifier = line[len(state):].strip().split()[0]
        is_symbolic = self.is_symbolic(identifier)
        if is_symbolic: #is symbolic
            word = identifier
            menu = line[:len(state) + len(identifier) + 1]
        else:
            word = identifier[:-1]
            menu = line[:len(state) + len(identifier)]

        d = {'word': word,
             'menu': menu,
             'info': [line]}
        return (state, d)

    def _struct(self, line, state, **kw):
        identifier = line[len(state):].strip().split()[0]
        is_symbolic = self.is_symbolic(identifier)
        if is_symbolic:
            word = identifier
        else:
            word = identifier[:-1]
        d = {'word': word,
             'menu': line.strip(),
             'info': [line]}
        return (state, d)

    def is_symbolic(self, identifier):
        """ Check if the identifier suffix is symbolic.
        """
        is_symbolic = True
        if len(identifier) > 1:
            penultimate = identifier[-2]
            if penultimate.isalnum() or penultimate in ["'", "_"]: # exclude "." !
                is_symbolic = False
        return is_symbolic

if __name__ == "__main__":
    """ To run:
            cd ..
            python -m parsers.basisparser
    """
    fpath = '/home/max/projects/schmerlin/test/.ide/example.smlb.basis'
    parser = BasisParser(fpath, 1)
    print(parser.parse())
