import vim
import os

CURDIR = os.path.dirname(os.path.realpath(__file__))
KW_FILE = 'data/keywords'

# TODO: naive matcher, rewrite with prefix trie cached on disk
def complete_prefix(base):
    with open(os.path.join(CURDIR, KW_FILE), 'r') as infile:
        keywords = infile.readlines()
        res = [{"word": kw.strip(), "abbr": kw.strip(), "icase": 1} \
                    for kw in keywords \
                    if kw[:len(base)].lower() == base.lower()]
        return res
