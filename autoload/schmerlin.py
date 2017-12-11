import os
from trie import Trie
import pickle

CURDIR = os.path.dirname(os.path.realpath(__file__))
KW_FILE = 'data/keywords' # will be pickled on disk under .pkl extension

# store module level buffer info
# TODO: store buffer path & timestamp
class Cache:
    pass
__cache = Cache()
__cache.buffer = None



def load_trie():
    """ Load prefix trie from pickled file into module cache.
    """
    if __cache.buffer is not None:
        return

    if os.path.exists(os.path.join(CURDIR, KW_FILE + '.pkl')):
        __cache.buffer = pickle.load(
                                open(os.path.join(CURDIR, KW_FILE + '.pkl'), 'rb'))
    __cache.buffer = parse_trie()

def parse_trie():
    """ Create prefix trie from flat ASCII file.
    """
    tr = Trie()
    with open(os.path.join(CURDIR, KW_FILE), 'r') as infile:
        for kw in infile.readlines():
            tr.insert(kw.strip())
        pickle.dump(tr,
                    open(os.path.join(CURDIR, KW_FILE + '.pkl'), 'wb'),
                    protocol=pickle.HIGHEST_PROTOCOL)
    return tr

def complete_prefix(base):
    """ Autocomplete from prefix and trie.
    """
    tr = __cache.buffer
    res = [{"word": word, "abbr": word, "kind": "⚷"} \
                for word in tr.autocomplete(base)]
    return res

if __name__ == "__main__":
    load_trie()
    res = complete_prefix('a')
    print(res)
