import os
from trie import Trie
import pickle
from basisparser import Parser

CURDIR = os.path.dirname(os.path.realpath(__file__))
KW_FILE = 'data/keywords' # will be pickled on disk under .pkl extension

# store module level buffer info
# TODO: store buffer path & timestamp
class Cache:
    pass
__cache = Cache()
__cache.buffer = None



def load_trie(fpath):
    """ Load prefix trie from pickled file into module cache.
    """

    if __cache.buffer is not None:
        return

    # # TODO: TESTING..
    # print(fpath)
    # __cache.buffer = []
    # return

    # TODO: working here...
    basis = Parser(fpath).parse()

    if os.path.exists(os.path.join(CURDIR, KW_FILE + '.pkl')):
        __cache.buffer = pickle.load(
                                open(os.path.join(CURDIR, KW_FILE + '.pkl'), 'rb'))
    __cache.buffer = parse_trie(basis)

def parse_trie(basis):
    """ Create prefix trie from flat ASCII file.
    """
    tr = Trie()
    # insert basis
    for item in basis:
        tr.insert(item)
    # insert keywords
    with open(os.path.join(CURDIR, KW_FILE), 'r') as infile:
        for kw in infile.readlines():
            tr.insert({"word": kw.strip(),
                       "kind": "[⚷]",
                       "menu": "<reserved keyword>"})
        pickle.dump(tr,
                    open(os.path.join(CURDIR, KW_FILE + '.pkl'), 'wb'),
                    protocol=pickle.HIGHEST_PROTOCOL)
    return tr

def complete_prefix(base):
    """ Autocomplete from prefix and trie.
    """
    tr = __cache.buffer
    # # TODO: dummy
    # print(tr.autocomplete(base))
    # return []
    return sorted(tr.autocomplete(base), key = lambda item: item['word'])

if __name__ == "__main__":
    fpath = '/home/max/projects/schmerlin/autoload/example.smlb'
    load_trie(fpath)
    res = complete_prefix('a')
    print(res)
