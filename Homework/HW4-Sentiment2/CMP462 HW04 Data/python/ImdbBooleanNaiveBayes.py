import math


class ImdbBooleanNaiveBayes:
    def __init__(self):
        self.boolean_naive_bayes_pos = {}
        self.boolean_naive_bayes_neg = {}
        self.word_count_pos = 0
        self.word_count_neg = 0
        self.doc_count_pos = 0
        self.doc_count_neg = 0
        self.V = set()

    def add_words(self, klass, words):
        if klass == 'pos':
            self.doc_count_pos += 1
            for word in words:
                self.boolean_naive_bayes_pos[word] = 1
                self.word_count_pos += 1
                self.V.add(word)
        else:
            self.doc_count_neg += 1
            for word in words:
                self.boolean_naive_bayes_neg[word] = 1
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
            if word not in self.boolean_naive_bayes_pos:
                score_pos = float('-inf')
            else:
                score_pos += math.log(self.boolean_naive_bayes_pos.get(word, 0) + 1)
                score_pos -= total_log_pos

            if word not in self.boolean_naive_bayes_neg:
                score_neg = float('-inf')
            else:
                score_neg += math.log(self.boolean_naive_bayes_neg.get(word, 0) + 1)
                score_neg -= total_log_neg

        return score_pos, score_neg
