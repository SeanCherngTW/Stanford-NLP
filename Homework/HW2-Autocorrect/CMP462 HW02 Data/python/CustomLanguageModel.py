import math
import collections


class CustomLanguageModel:

    """
    Good-Turing
    P*GT(word) = c* / N
    c* = (c+1)(Nc+1) / (Nc)

    Advanced Good-Turing
    c* = c   (if c > k)
    c* = ... (if 0 <= c <= k)
    """

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.unigramCounts = collections.defaultdict(lambda: 0)
        self.goodTuring = {}
        self.goodTuringCounts = collections.defaultdict(lambda: 0)
        self.total = 0
        self.init_good_turing()
        self.train(corpus)

    def init_good_turing(self):
        self.goodTuring[0] = 0.000027
        self.goodTuring[1] = 0.446
        self.goodTuring[2] = 1.26
        self.goodTuring[3] = 2.24
        self.goodTuring[4] = 3.24
        self.goodTuring[5] = 4.22
        self.goodTuring[6] = 5.19
        self.goodTuring[7] = 6.21
        self.goodTuring[8] = 7.24
        self.goodTuring[9] = 8.25

    def train(self, corpus):
        """ Takes a corpus and trains your language model.
            Compute any counts or other corpus statistics in this function.
        """
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.unigramCounts[token] += 1
                self.total += 1

        # add-one smoothing
        # self.total += len(self.laplaceUnigramCounts.keys())

        for k, v in self.unigramCounts.items():
            self.goodTuringCounts[v] += 1

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the
            sentence using your language model. Use whatever data you computed in train() here.
        """
        score = 0.0
        for token in sentence:
            count = self.unigramCounts[token]
            if count == 0:
                score += self.goodTuring[1] / self.total
            elif 0 < count < 10:
                c_star = self.goodTuring[count]
                score += c_star / self.total
            else:
                c_star = count - 0.75
                score += c_star / self.total
        return score
