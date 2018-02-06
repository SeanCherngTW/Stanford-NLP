# -*- coding: utf-8 -*-

import math
import collections


class LaplaceBigramLanguageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.laplaceUnigramCounts = collections.defaultdict(lambda: 0)
        self.laplaceBigramCounts = collections.defaultdict(lambda: 0)
        self.V = 0
        self.train(corpus)

    def train(self, corpus):
        """ Takes a corpus and trains your language model.
            Compute any counts or other corpus statistics in this function.
        """
        for sentence in corpus.corpus:
            first_token = sentence.data[0].word
            for token in sentence.data[1:]:
                second_token = token.word
                self.laplaceUnigramCounts[first_token] += 1
                self.laplaceBigramCounts[first_token, second_token] += 1
                first_token = second_token

        # add-one smoothing
        self.V += len(self.laplaceBigramCounts.keys())

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the
            sentence using your language model. Use whatever data you computed in train() here.

            log(P(wn∣wn−1)) = log(C(wn−1,wn)+1 / C(wn−1)+V)
            log(P(wn∣wn−1)) = log(C(wn−1,wn)+1) - log(C(wn−1)+V)
            V is the number of distinct bigram
        """
        score = 0.0
        first_token = sentence[0]
        for second_token in sentence[1:]:
            unigram_count = self.laplaceUnigramCounts[second_token]
            bigram_count = self.laplaceBigramCounts[first_token, second_token]
            bigram_uni_count = self.laplaceUnigramCounts[first_token]

            score += math.log(bigram_count + 1)  # log(C(wn−1,wn)+1)
            score -= math.log(bigram_uni_count + self.V)  # -log(C(wn−1)+V)

            first_token = second_token
        return score
