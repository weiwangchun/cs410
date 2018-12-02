import statistics
import nltk
from nltk.classify import ClassifierI
from nltk.tokenize import word_tokenize


def find_features(features_list, term):
    words = word_tokenize(term)
    features = {}
    for w in features_list:
        features[w] = (w in words)

    return features

def find_max_mode(list1):
    list_table = statistics._counts(list1)
    len_table = len(list_table)

    if len_table == 1:
        max_mode = statistics.mode(list1)
    else:
        new_list = []
        for i in range(len_table):
            new_list.append(list_table[i][0])
        max_mode = max(new_list) # use the max value here
    return max_mode

class selectClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for x in self._classifiers:
            v = x.classify(features)
            votes.append(v)
        return find_max_mode(votes)

    def confidence(self, features):
        votes = []
        for x in self._classifiers:
            v = x.classify(features)
            votes.append(v)

        choice_votes = votes.count(find_max_mode(votes))
        conf = choice_votes / len(votes)
        return conf
