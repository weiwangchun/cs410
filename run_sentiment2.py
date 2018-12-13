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
import random
import sys
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
    # only use word features in Loughran McDonald

    return word_features


# extract features from a document
def extract_features(document):
    document_words= set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word]= (word in document_words)
    return features



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Please provide mda.pickle and portion_of_data_for_training. \nFor Example: >python run_sentiment.py mda.pickle 0.80")
        sys.exit(1)

    mda_file = sys.argv[1]
    pct_training_data = float(sys.argv[2])

    # define word features based on words identified by Loughran McDonald
    # download master dictionary - isolate only positive and negative words
    MASTER_DICT = pd.read_excel("master_dictionary.xlsx")
    wordlist = MASTER_DICT.loc[(MASTER_DICT['Negative']!= 0) | (MASTER_DICT['Positive']!= 0) ]['Word']
    word_features = get_word_features(wordlist.tolist())

    # mda file consists of word_list and sentiment
    with open('stock_files/mda_reports/' + mda_file,'rb') as f:
        mda = pickle.load(f)

    # remove items in the mda list with less than 5 words
    # this removes cases where we were unable to extract the MD&A section properly
    mda = [item for item in mda if len(item[0]) >= 5 ]
    # randomize the list
    random.shuffle(mda)

    #word_features = get_word_features(get_words_in_mda(mda))
    
    # define training set
    training_set= nltk.classify.apply_features(extract_features, mda[0:int(len(mda) * pct_training_data)] )
    # define test set
    test_set= nltk.classify.apply_features(extract_features, mda[int(len(mda) * pct_training_data + 1):(len(mda) - 1)] )
    
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


    # Evaluation Stage
    # split test set 
    positive_test = [item for item in test_set if item[1] == 'Positive']
    negative_test = [item for item in test_set if item[1] == 'Negative']

    # work out precision, recall and f scores
    recall_nb = nltk.classify.accuracy(classifier_nb, positive_test) 
    precision_nb = ((1 - nltk.classify.accuracy(classifier_nb, negative_test)) * len(negative_test)) / (recall_nb * len(positive_test) +  (1 - nltk.classify.accuracy(classifier_nb, negative_test)) * len(negative_test))
    f_nb = (2*recall_nb*precision_nb)/(recall_nb + precision_nb)

    recall_mnb = nltk.classify.accuracy(classifier_mnb, positive_test) 
    precision_mnb = ((1 - nltk.classify.accuracy(classifier_mnb, negative_test)) * len(negative_test)) / (recall_mnb * len(positive_test) +  (1 - nltk.classify.accuracy(classifier_mnb, negative_test)) * len(negative_test))
    f_mnb = (2*recall_mnb*precision_mnb)/(recall_mnb + precision_mnb)

    recall_bnb = nltk.classify.accuracy(classifier_bnb, positive_test) 
    precision_bnb = ((1 - nltk.classify.accuracy(classifier_bnb, negative_test)) * len(negative_test)) / (recall_bnb * len(positive_test) +  (1 - nltk.classify.accuracy(classifier_bnb, negative_test)) * len(negative_test))
    f_bnb = (2*recall_bnb*precision_bnb)/(recall_bnb + precision_bnb)

    recall_lr = nltk.classify.accuracy(classifier_lr, positive_test) 
    precision_lr = ((1 - nltk.classify.accuracy(classifier_lr, negative_test)) * len(negative_test)) / (recall_lr * len(positive_test) +  (1 - nltk.classify.accuracy(classifier_lr, negative_test)) * len(negative_test))
    f_lr = (2*recall_lr*precision_lr)/(recall_lr + precision_lr)

    recall_sgd = nltk.classify.accuracy(classifier_sgd, positive_test) 
    precision_sgd = ((1 - nltk.classify.accuracy(classifier_sgd, negative_test)) * len(negative_test)) / (recall_sgd * len(positive_test) +  (1 - nltk.classify.accuracy(classifier_sgd, negative_test)) * len(negative_test))
    f_sgd = (2*recall_sgd*precision_sgd)/(recall_sgd + precision_sgd)

    recall_svc = nltk.classify.accuracy(classifier_svc, positive_test) 
    precision_svc = ((1 - nltk.classify.accuracy(classifier_svc, negative_test)) * len(negative_test)) / (recall_svc * len(positive_test) +  (1 - nltk.classify.accuracy(classifier_svc, negative_test)) * len(negative_test))
    f_svc = (2*recall_svc*precision_svc)/(recall_svc + precision_svc)

    # test sample accuracy
    print("Naive Bayes classifier precision:", precision_nb, "recall:", recall_nb, "f1-score:", f_nb)
    print("Multinomial Naive Bayes classifier  precision:", precision_mnb, "recall:", recall_mnb, "f1-score:", f_mnb)
    print("Bernoulli Naive Bayes precision:", precision_bnb, "recall:", recall_bnb, "f1-score:", f_bnb)
    print("Losistic Regression classifier  precision:", precision_lr, "recall:", recall_lr, "f1-score:", f_lr)
    print("SGD classifier precision:", precision_sgd, "recall:", recall_sgd, "f1-score:", f_sgd)
    print("SVC classifier precision:", precision_svc, "recall:", recall_svc, "f1-score:", f_svc)

    print("Naive Bayes classifier  accuracy pct:", (nltk.classify.accuracy(classifier_nb, test_set))*100)
    print("Multinomial Naive Bayes classifier accuracy pct:", (nltk.classify.accuracy(classifier_mnb, test_set))*100)
    print("Bernoulli Naive Bayes  accuracy pct:", (nltk.classify.accuracy(classifier_bnb, test_set))*100)
    print("Losistic Regression classifier  accuracy pct:", (nltk.classify.accuracy(classifier_lr, test_set))*100)
    print("SGD classifier accuracy pct:", (nltk.classify.accuracy(classifier_sgd, test_set))*100)
    print("SVC classifier accuracy pct:", (nltk.classify.accuracy(classifier_svc, test_set))*100)

    # save classifiers for future use
    with open('stock_files/mda_reports/classifiers.pickle', 'wb') as f:
        pickle.dump(classifier_nb, f)
        pickle.dump(classifier_mnb, f)
        pickle.dump(classifier_bnb, f)
        pickle.dump(classifier_lr, f)
        pickle.dump(classifier_sgd, f)
        pickle.dump(classifier_svc, f)
    f.close()

    # classify
    #with open('stock_files/mda_reports/52795_ANIXTER INTERNATIONAL INC_10-K_2017-02-23.txt', 'r') as myfile:
    #    data=myfile.read().replace('\n', '')
    #classifier_svc.classify(extract_features(data.split()))







