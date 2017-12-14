from .parser import Parser

class KWParser(Parser):
    SYM = '⚷'
    MENU = '<reserved>'
    INFO = ' '

    def __init__(self, fpath, dup):
        """ Receives path to keywords file and DUP flag.
        """
        super(KWParser, self).__init__(fpath, dup)

    def parse(self):
        with open(self.fpath, 'r') as infile:
            res = [{"word": line.strip(),
                    "kind": "[%s]" %self.SYM,
                    "menu": self.MENU,
                    "info": self.INFO,
                    "dup": self.DUP}
                   for line in infile.readlines()]

            return res

if __name__ == "__main__":
    """ To run:
            cd ..
            python -m parsers.keywordparser
    """
    fpath = './data/keywords'
    print(KWParser(fpath, 1).parse())
