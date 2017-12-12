from functools import reduce
import json

class Trie:
    def __init__(self):
        """ A trie is a recursive datastructure that has zero or more
            tries as its follow.
        """
        self.follow = {}
        self.is_sentinel = False # True for char at end of word
        self.item = None

    def autocomplete(self, prefix):
        """ For now returns a flat unsorted list of words.
        """
        char = self
        # match prefix
        for letter in prefix:
            if letter not in char.follow:
                return []
            char = char.follow[letter]

        # return list(char._expand(prefix))
        return [json.loads(item) for item in char._expand(prefix)]

    def _expand(self, prefix):
        res = set()
        if self.is_sentinel:
            res.add(json.dumps(self.item))
        res = reduce(
            lambda acc, elem: acc.union(elem),
            [subtrie._expand(prefix + char) for (char, subtrie) in self.follow.items()],
            res)
        return res

    def insert(self, item):
        """ Insert a string into a trie.
        """
        string = item['word']
        if not string: # empty
            return
        char = self
        for letter in string:
            if letter not in char.follow:
                char.follow[letter] = Trie()
            char = char.follow[letter]
        char.is_sentinel = True
        char.item = item

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
