from functools import reduce

class Trie:
    def __init__(self):
        """ A trie is a recursive datastructure that has zero or more
            tries as its follow.
        """
        self.follow = {}
        self.is_sentinel = False # True for char at end of word

    def autocomplete(self, prefix):
        """ For now returns a flat unsorted list of words.
        """
        char = self
        # match prefix
        for letter in prefix:
            if letter not in char.follow:
                return []
            char = char.follow[letter]

        return list(char._expand(prefix))

    def _expand(self, prefix):
        res = set()
        if self.is_sentinel:
            res.add(prefix)
        res = reduce(
            lambda acc, elem: acc.union(elem),
            [subtrie._expand(prefix + char) for (char, subtrie) in self.follow.items()],
            res)
        return res

    def insert(self, string):
        """ Inster a string into a trie.
        """
        if not string: # empty
            return
        char = self
        for letter in string:
            if letter not in char.follow:
                char.follow[letter] = Trie()
            char = char.follow[letter]
        char.is_sentinel = True

    # TODO: implement https://pdfs.semanticscholar.org/ed71/b0b2bb44289e41807a740d4cfbcfdd7f6372.pdf
    def dump(self):
        pass
    def load(self):
        pass

if __name__ == "__main__":
    t = Trie()
    dictionary = ["A","to", "tea", "ted", "ten", "I", "in", "inn"]
    for word in dictionary:
        t.insert(word)
    print(t.autocomplete('Z')) # => []
    print(t.autocomplete('t')) # => ['to', 'tea', ted', 'ten']
    print(t.autocomplete('te')) # => ['tea', 'ted', 'ten']
    print(t.autocomplete('A')) # => ['A']
    print(t.autocomplete('I')) # => ['I']
    print(t.autocomplete('i')) # => ['in', 'inn']
