import os
import pickle
from util.trie import Trie
from parsers.basisparser import BasisParser
from parsers.keywordparser import KWParser

CURDIR = os.path.dirname(os.path.realpath(__file__))
KW_FILE = 'data/keywords' # will be pickled on disk under .pkl extension
BASIS_DIR = '.ide'
PKL_EXT = '.pkl' # pickled file ext
BASIS_EXT = '.basis'

# :help complete-items
#   when non-zero this match will be added even when an item
#   with the same word is already present
DUP = 1

# cache trie for each buffer in memory
class Cache:
    pass
__cache = Cache()
__cache.buffer = {} # {"/path/to/file":Trie()}


def get_trie(fpath): # from cache
    """ fpath is path to filename in buffer (string).
    """
    fpath = os.path.normpath(fpath)
    return __cache.buffer.setdefault(fpath, cache_trie(fpath))

def path_to_pickle(fpath):
    success = True
    pickle_fname = os.path.basename(fpath) + PKL_EXT
    pth = os.path.join(
            os.path.dirname(fpath),
            BASIS_DIR,
            pickle_fname)
    if not os.path.exists(pth):
        success = False
    return success, pth


def cache_trie(fpath): # from pickled store
    """ fpath is path to filename in buffer (string).
    """
    success, pth = path_to_pickle(fpath)
    if success:
        __cache.buffer[fpath] = pickle.load(open(pth, 'rb'))
        return __cache.buffer[fpath]
    return force_load_trie(fpath)

def force_load_trie(fpath): # from .mlb file
    """ Run MLton, parse, create Trie, dump to pickled store & cache.
    """
    # run mlton with -show-basis
    dump_basis(fpath)

    _, pth_pkl = path_to_pickle(fpath)
    pth_kw = os.path.join(
                CURDIR,
                KW_FILE)
    pth_bas = os.path.join(
                os.path.dirname(fpath),
                BASIS_DIR,
                os.path.basename(fpath) + BASIS_EXT)
    res = KWParser(pth_kw, DUP).parse()
    res.extend(BasisParser(pth_bas, DUP).parse())

    # for now sorting only in lexicographic order
    tr = Trie()
    for obj in sorted(res, key=lambda x: x['word']):
        tr.insert(obj)
    pickle.dump(tr,
                open(pth_pkl, 'wb'),
                protocol=pickle.HIGHEST_PROTOCOL)
    __cache.buffer[fpath] = tr
    return tr


def complete_prefix(base, fpath):
    """ Autocomplete from prefix for path.
    """
    tr = get_trie(fpath)
    return tr.autocomplete(base)

# TODO
# run mlton -show-basis
def dump_basis(fpath):
    pass

if __name__ == "__main__":
    fpath = '/home/max/projects/schmerlin/test/example.smlb'
    print(complete_prefix('a', fpath))
