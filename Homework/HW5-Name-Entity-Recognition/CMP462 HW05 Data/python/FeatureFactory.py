import re
import sys
import json
import nltk
import base64
import string
from Datum import Datum

captial_pat = '^[A-Z][a-z]+$'
camel_pat = '^([A-Z][a-z]+)+$'
double_pat = '^[A-Za-z]+-[A-Za-z]+$'


class FeatureFactory:
    """
    Add any necessary initialization steps for your features here
    Using this constructor is optional. Depending on your
    features, you may not need to intialize anything.
    """

    def __init__(self):
        pass

    """
    Words is a list of the words in the entire corpus, previousLabel is the label
    for position-1 (or O if it's the start of a new sentence), and position
    is the word you are adding features for. PreviousLabel must be the
    only label that is visible to this method.
    """

    def isPunctuation(self, s):
        for c in s:
            if c not in string.punctuation:
                return False
        return True

    def wordPattern(self, s):
        if s.isupper():
            return 'ALLCAP'
        elif s.islower():
            return 'lower'
        elif re.match(captial_pat, s):
            return 'Captial'
        elif re.match(camel_pat, s):
            return 'Camel'
        elif re.match(double_pat, s):
            return 'Double'
        else:
            return 'Others'

    def wordPrefix(self, s):
        # s[:3] gives the best performance
        return re.sub(r"[^a-zA-Z\.\,\!\?]", "#", s[:3])

    def wordSuffix(self, s):
        # s[-3:] gives the best performance
        return re.sub(r"[^a-zA-Z\.\,\!\?]", "#", s[-3:])

    def posTag(self, s):
        return nltk.pos_tag([s])[0][1]

    def isNoun(self, s):
        return True if self.posTag(s).startswith('N') else False

    def hasDigit(self, s):
        for c in s:
            if c.isdigit():
                return True
        return False

    def computeFeatures(self, words, previousLabel, position):
        features = []
        currentWord = words[position]

        """ Baseline Features """
        features.append("word=" + currentWord)
        # features.append("prevLabel=" + previousLabel)
        features.append("word=" + currentWord + ", prevLabel=" + previousLabel)
        """
        Warning: If you encounter "line search failure" error when
        running the program, considering putting the baseline features
        back. It occurs when the features are too sparse. Once you have
        added enough features, take out the features that you don't need.
        """

        """ TODO: Add your features here """
        features.append("isdigit=" + str(self.hasDigit(currentWord)))
        features.append("isPunc=" + str(self.isPunctuation(currentWord)))
        features.append("len=" + str(len(currentWord)))
        # features.append("isNoun=" + str(self.isNoun(currentWord)))
        wp = self.wordPattern(currentWord)
        features.append("prevLabel=" + previousLabel + ", pattern=" + wp)
        features.append("prefix3=" + self.wordPrefix(currentWord))
        features.append("suffix3=" + self.wordSuffix(currentWord))

        return features

    """ Do not modify this method """

    def readData(self, filename):
        data = []

        for line in open(filename, 'r'):
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data

    """ Do not modify this method """

    def readTestData(self, ch_aux):
        data = []

        for line in ch_aux.splitlines():
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data

    """ Do not modify this method """

    def setFeaturesTrain(self, data):
        newData = []
        words = []

        for datum in data:
            words.append(datum.word)

        # This is so that the feature factory code doesn't
        # accidentally use the true label info
        previousLabel = "O"
        for i in range(0, len(data)):
            datum = data[i]

            newDatum = Datum(datum.word, datum.label)
            newDatum.features = self.computeFeatures(words, previousLabel, i)
            newDatum.previousLabel = previousLabel
            newData.append(newDatum)

            previousLabel = datum.label

        return newData

    """
    Compute the features for all possible previous labels
    for Viterbi algorithm. Do not modify this method
    """

    def setFeaturesTest(self, data):
        newData = []
        words = []
        labels = []
        labelIndex = {}

        for datum in data:
            words.append(datum.word)
            if datum.label not in labelIndex:
                labelIndex[datum.label] = len(labels)
                labels.append(datum.label)

        # This is so that the feature factory code doesn't
        # accidentally use the true label info
        for i in range(0, len(data)):
            datum = data[i]

            if i == 0:
                previousLabel = "O"
                datum.features = self.computeFeatures(words, previousLabel, i)

                newDatum = Datum(datum.word, datum.label)
                newDatum.features = self.computeFeatures(words, previousLabel, i)
                newDatum.previousLabel = previousLabel
                newData.append(newDatum)
            else:
                for previousLabel in labels:
                    datum.features = self.computeFeatures(words, previousLabel, i)

                    newDatum = Datum(datum.word, datum.label)
                    newDatum.features = self.computeFeatures(words, previousLabel, i)
                    newDatum.previousLabel = previousLabel
                    newData.append(newDatum)

        return newData

    """
    write words, labels, and features into a json file
    Do not modify this method
    """

    def writeData(self, data, filename):
        outFile = open(filename + '.json', 'w')
        for i in range(0, len(data)):
            datum = data[i]
            jsonObj = {}
            jsonObj['_label'] = datum.label
            jsonObj['_word'] = base64.b64encode(datum.word)
            jsonObj['_prevLabel'] = datum.previousLabel

            featureObj = {}
            features = datum.features
            for j in range(0, len(features)):
                feature = features[j]
                featureObj['_' + feature] = feature
            jsonObj['_features'] = featureObj

            outFile.write(json.dumps(jsonObj) + '\n')

        outFile.close()
