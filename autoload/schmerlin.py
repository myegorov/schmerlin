import vim

# TODO: naive matcher, rewrite with prefix trie cached on disk
def complete_prefix(base):
    with open('data/keywords', 'r') as infile:
        keywords = infile.readlines()
        res = [{'word': kw, 'abbr': kw, 'icase': 1} \
                    for kw in keywords \
                    if kw[:len(base)].lower() == base.lower()]
        return repr(res)
