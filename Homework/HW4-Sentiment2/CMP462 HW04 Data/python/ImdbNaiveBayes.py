import math


class ImdbNaiveBayes:
    def __init__(self):
        self.naive_bayes_pos = {}
        self.naive_bayes_neg = {}
        self.word_count_pos = 0
        self.word_count_neg = 0
        self.doc_count_pos = 0
        self.doc_count_neg = 0
        self.V = set()

    def add_words(self, klass, words):
        if klass == 'pos':
            self.doc_count_pos += 1
            for word in words:
                self.naive_bayes_pos[word] = self.naive_bayes_pos.get(word, 0) + 1
                self.word_count_pos += 1
                self.V.add(word)
        else:
            self.doc_count_neg += 1
            for word in words:
                self.naive_bayes_neg[word] = self.naive_bayes_neg.get(word, 0) + 1
                self.word_count_neg += 1
                self.V.add(word)

    def init_score(self):
        doc_count_total = self.doc_count_pos + self.doc_count_neg
        init_score_pos = math.log(float(self.doc_count_pos) / doc_count_total)
        init_score_neg = math.log(float(self.doc_count_neg) / doc_count_total)
        return init_score_pos, init_score_neg

    def get_score(self, words):
        score_pos, score_neg = self.init_score()
        total_log_pos = math.log(self.word_count_pos + len(self.V))
        total_log_neg = math.log(self.word_count_neg + len(self.V))
        for word in words:
            score_pos += math.log(self.naive_bayes_pos.get(word, 0) + 1)
            score_pos -= total_log_pos
            score_neg += math.log(self.naive_bayes_neg.get(word, 0) + 1)
            score_neg -= total_log_neg
        return score_pos, score_neg
