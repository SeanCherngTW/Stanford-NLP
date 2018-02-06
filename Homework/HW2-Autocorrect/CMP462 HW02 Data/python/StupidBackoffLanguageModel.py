import math
import collections


class StupidBackoffLanguageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        self.unigramCounts = collections.defaultdict(lambda: 0)
        self.bigramCounts = collections.defaultdict(lambda: 0)
        self.trigramCounts = collections.defaultdict(lambda: 0)
        self.unigram_total = 0
        self.train(corpus)

    def train(self, corpus):
        """ Takes a corpus and trains your language model.
            Compute any counts or other corpus statistics in this function.
        """
        for sentence in corpus.corpus:
            first_token = sentence.data[0].word
            second_token = sentence.data[1].word

            for token in sentence.data[2:]:
                third_token = token.word
                self.unigram_total += 1
                self.unigramCounts[first_token] += 1
                self.bigramCounts[first_token, second_token] += 1
                self.trigramCounts[first_token, second_token, third_token] += 1
                first_token, second_token = second_token, third_token

        # add-one smoothing for unigram
        self.unigram_total += len(self.unigramCounts.keys())

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the
            sentence using your language model. Use whatever data you computed in train() here.
        """
        score = 0.0
        length = len(sentence)
        first_token = sentence[0]
        second_token = sentence[1]

        for third_token in sentence[2:]:
            unigram_count = self.unigramCounts[third_token]
            bigram_count = self.bigramCounts[second_token, third_token]
            bigram_uni_count = self.unigramCounts[second_token]
            trigram_count = self.trigramCounts[first_token, second_token, third_token]
            trigram_bi_count = self.bigramCounts[(first_token, second_token)]

            if trigram_count > 0:
                score += math.log(trigram_count)
                score -= math.log(trigram_bi_count)

            elif bigram_count > 0:
                # score += math.log(0.4)
                score += math.log(bigram_count)
                score -= math.log(bigram_uni_count)

            else:
                # score += math.log(0.16)
                score += math.log(unigram_count + 1)
                score -= math.log(self.unigram_total)

            first_token, second_token = second_token, third_token
        return score
