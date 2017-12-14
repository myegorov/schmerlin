from functools import reduce
from collections import OrderedDict

class Trie:

    KEY = 'word'

    def __init__(self):
        """ A trie is a recursive datastructure that has zero or more
            tries as its follow.
        """
        # order of insertion matters!
        self.follow = OrderedDict()
        self.leaves = None # [obj...] for char at end of word


    def insert(self, item):
        """ Insert an obj into a trie (ordered for retrieval by self.KEY)
        """
        string = item[self.KEY]
        char = self
        for letter in string:
            char.follow.setdefault(letter, Trie())
            char = char.follow[letter]

        # may store distinct objects with identical self.KEY
        if char.leaves is None:
            char.leaves = [item]
        else:
            char.leaves.append(item)


    def autocomplete(self, prefix):
        """ Returns a (sorted by insertion order) list of objects
            whose object[self.KEY] starts with prefix.
        """
        char = self
        # consume prefix
        for letter in prefix:
            if letter not in char.follow:
                return []
            char = char.follow[letter]

        # autocomplete suffixes
        return char._expand(prefix)


    def _expand(self, prefix):
        res = []
        if self.leaves is not None:
            res.extend(self.leaves)
        res = reduce(
            lambda acc, leaves: acc + leaves,
            [subtrie._expand(prefix + char) for (char, subtrie) in self.follow.items()],
            res)
        return res


if __name__ == "__main__":
    t = Trie()
    dictionary = ["A","to", "tea", "ted", "ten", "I", "in", "inn"]
    for word in sorted(dictionary):
        t.insert({t.KEY: word})
    print(t.autocomplete('Z')) # => []
    print(t.autocomplete('t')) # => ['tea', 'ted', 'ten', 'to']
    print(t.autocomplete('te')) # => ['tea', 'ted', 'ten']
    print(t.autocomplete('A')) # => ['A']
    print(t.autocomplete('I')) # => ['I']
    print(t.autocomplete('i')) # => ['in', 'inn']
