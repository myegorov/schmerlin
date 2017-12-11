import os
from trie import Trie

CURDIR = os.path.dirname(os.path.realpath(__file__))
KW_FILE = 'data/keywords'

# TODO: load prefix trie from disk
def load_trie():
    """ For now return lists of keywords ([str])
    """
    t = Trie()
    with open(os.path.join(CURDIR, KW_FILE), 'r') as infile:
        for kw in infile.readlines():
            t.insert(kw.strip())
    return t

# TODO: naive matcher, rewrite with prefix trie cached on disk
def complete_prefix(base, tr = None):
    if not tr:
        raise ValueError("Got empty prefix trie")
    res = [{"word": word, "abbr": word, "kind": "⚷"} \
                for word in tr.autocomplete(base)]
    return res
