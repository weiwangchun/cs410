import pandas as pd
import random
import clasfuncdef as cfd
import nltk
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

print("Importing Positive Terms..")
positive_terms = open("Positive Terms.csv","r").read()
print("Import Positive Terms complete !!")

print("")
print("Importing Negative Terms..")
negative_terms = open("Negative Terms.csv","r").read()
print("Import Negative Terms complete !!")
print("")


print("Importing Comments whose sentiment shall be analysed..")
print("")
print("Enter TestPositive.txt to analyse a Positive sample")
print("Enter TestNegative.txt to analyse a Negative sample")
print("")

fname = input("Enter file name to analyze the sentiment: ")

try:
    src_comments = open(fname,"r").read()
except Exception as e:
    print('Unable to read the file !!')
    exit()

print('Building FeatureSet..')
# Build Vocabulary and collect sample Positive, Negative terms
terms_collection = []
vocabulary = []

for r in positive_terms.split('\n'):
    terms_collection.append( (r, "positive") )
    vocabulary.append(r.lower())

for r in negative_terms.split('\n'):
    terms_collection.append( (r, "negative") )
    vocabulary.append(r.lower())

vocabulary = nltk.FreqDist(vocabulary)
features_list = list(vocabulary.keys())
featuresets = [(cfd.find_features(features_list, trm), category) for (trm, category) in terms_collection]
random.shuffle(featuresets)

print('FeatureSet determination complete !!')
print('')

set_training = featuresets[:50]
set_testing =  featuresets[50:]


NB_classifier = nltk.NaiveBayesClassifier.train(set_training)
print("Naive Bayes classifier accuracy %age:", (nltk.classify.accuracy(NB_classifier, set_testing))*100)
print('')

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(set_training)
print("MultinomialNB classifier accuracy %age:", (nltk.classify.accuracy(MNB_classifier, set_testing))*100)
print('')

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(set_training)
print("BernoulliNB classifier accuracy %age:", (nltk.classify.accuracy(BernoulliNB_classifier, set_testing))*100)
print('')

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(set_training)
print("LogisticRegression classifier accuracy %age:", (nltk.classify.accuracy(LogisticRegression_classifier, set_testing))*100)
print('')

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(set_training)
print("SGD classifier accuracy %age:", (nltk.classify.accuracy(SGDClassifier_classifier, set_testing))*100)
print('')

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(set_training)
print("LinearSVC classifier accuracy %age:", (nltk.classify.accuracy(LinearSVC_classifier, set_testing))*100)
print('')

selected_classifier = cfd.selectClassifier(
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

print("Selected Classifier accuracy %age:", (nltk.classify.accuracy(selected_classifier, set_testing))*100)
print('')

features_src_comments = cfd.find_features(features_list,src_comments)
print('')
print('Sentiment: ', selected_classifier.classify(features_src_comments).upper())
print('Sentiment Confidence: ', selected_classifier.confidence(features_src_comments)*100, ' %age')
