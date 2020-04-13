import random

MIN_WORD_LENGTH = 4
MAX_WORD_LENGTH = 10


class WordDatabase(object):
    _words = []

    def check_valid(self, word):
        _len = len(word)
        if MIN_WORD_LENGTH <= _len <= MAX_WORD_LENGTH:
            return all([ord('a') <= ord(c) <= ord('z') for c in word])
        else:
            return False

    def load(self, filename):
        self._words = []
        with open(filename, 'r') as fdr:
            for word in fdr.readlines():
                word = word.strip()
                if self.check_valid(word):
                    self._words.append(word)

    def get_random_word(self):
        return self._words[random.randint(0,len(self._words))]