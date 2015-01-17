import collections
import re
import string

class WordFixer(object):
    def __init__(self, word_file_path, additional_words = None):
        if not additional_words:
            additional_words = ""
        if isinstance(additional_words, (list, tuple, set)):
            additional_words = " " + string.join(list(additional_words))
        import logging
        logging.info(additional_words)
        self._NWORDS = self._train(self._words(file(word_file_path).read() + additional_words))
        self._numwords = { "and": (1, 0) }
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
            ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        for idx, word in enumerate(units):  self._numwords[word] = (1, idx)
        for idx, word in enumerate(tens):   self._numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): self._numwords[word] = (10 ** (idx * 3 or 2), 0)
    
    def _words(self, text):
        return re.findall('[a-z]+', text.lower()) 

    def _train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def _edits1(self, word):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def _known_edits2(self, word):
        return set(e2 for e1 in self._edits1(word) for e2 in self._edits1(e1) if e2 in self._NWORDS)

    def _known(self, words):
        return set(w for w in words if w in self._NWORDS)

    # From http://norvig.com/spell-correct.html
    def correct(self, original_word):
        word = original_word.lower()
        candidates = self._known([word]) or self._known(self._edits1(word)) or self._known_edits2(word) or [word]
        return max(candidates, key=self._NWORDS.get)

    def standardize_guess(self, guess):
        # Standardize numbers in answer
        guess = self.standardize_numbers(guess).upper()

        # Strip common phrases
        guess = re.sub('^(THE|AN|A) ', '', guess)
        guess = re.sub(' & ', ' AND ', guess)
        import logging
        logging.info(guess)
        # Replace CAMPBELL'S WITH CAMPBELLS
        guess = re.sub("([A-Z])'S\\b", "\\1S", guess)
        logging.info(guess)

        return guess

    # From http://stackoverflow.com/a/598322/399704
    def standardize_numbers(self, original):
        ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
        ordinal_endings = [('ieth', 'y'), ('th', '')]

        textnum = original.lower().replace('-', ' ')

        current = result = 0
        for word in textnum.split():
            if word in ordinal_words:
                scale, increment = (1, ordinal_words[word])
            else:
                for ending, replacement in ordinal_endings:
                    if word.endswith(ending):
                        word = "%s%s" % (word[:-len(ending)], replacement)

                if word not in self._numwords:
                    # Give up parsing
                    return original

                scale, increment = self._numwords[word]

            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0

        return str(result + current)
