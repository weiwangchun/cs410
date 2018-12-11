# CS410 UIUC - Run Sentiment Analysis
# Python 3
# Wang Chun Wei / Venkat Rao
# Open mda.pkl , define word features and run sentiment
# ----------------------------------------------------------------------------


import pickle
import glob
import csv
import numpy as np
import pandas as pd
import metapy
from itertools import chain
import nltk 
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.metrics import classification_report

def get_words_in_mda(mda):
    all_words = []
    for (words, sentiment) in mda:
        all_words.extend(words)
    return all_words

# word list features
def get_word_features(wordlist):
    wordlist= nltk.FreqDist(wordlist)  # wordlist contains frequencies
    word_features = wordlist.keys()
    return word_features


# extract features from a document
def extract_features(document):
    document_words= set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word]= (word in document_words)
    return features



if __name__ == '__main__':


    # mda file consists of word_list and sentiment
    with open('stock_files/mda_reports/mda.pickle','rb') as f:
        mda = pickle.load(f)

    # define word list
    word_features = get_word_features(get_words_in_mda(mda))
    # define training set
    training_set= nltk.classify.apply_features(extract_features, mda)
    # define test set
    test_set= nltk.classify.apply_features(extract_features, mda)
    
    # Run classifiers - Naive Bayes
    classifier_nb = nltk.classify.NaiveBayesClassifier.train(training_set) 
    # Multinomial Naive Bayes
    classifier_mnb = SklearnClassifier(MultinomialNB()).train(training_set)
    # Bernoulli Naive Bayes
    classifier_bnb = SklearnClassifier(BernoulliNB()).train(training_set)
    # Losistic Regression 
    classifier_lr = SklearnClassifier(LogisticRegression()).train(training_set)
    # Stochastic Gradient Descent
    classifier_sgd = SklearnClassifier(SGDClassifier(max_iter=5, tol=None)).train(training_set)
    # SVC
    classifier_svc = SklearnClassifier(LinearSVC()).train(training_set)

    # test sample accuracy
    print("Naive Bayes classifier accuracy %:", (nltk.classify.accuracy(classifier_nb, test_set))*100)
    print("Multinomial Naive Bayes classifier accuracy %:", (nltk.classify.accuracy(classifier_mnb, test_set))*100)
    print("Bernoulli Naive Bayes accuracy %:", (nltk.classify.accuracy(classifier_bnb, test_set))*100)
    print("Losistic Regression  classifier accuracy %:", (nltk.classify.accuracy(classifier_lr, test_set))*100)
    print("SGD classifier accuracy %:", (nltk.classify.accuracy(classifier_sgd, test_set))*100)
    print("SVC classifier accuracy %:", (nltk.classify.accuracy(classifier_svc, test_set))*100)


    # classify
    with open('stock_files/mda_reports/52795_ANIXTER INTERNATIONAL INC_10-K_2017-02-23.txt', 'r') as myfile:
        data=myfile.read().replace('\n', '')
    classifier.classify(extract_features(data.split()))