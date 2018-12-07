#!/usr/bin/env python
# coding: utf-8

# # Conducting Sentiment Analysis:

# Input: Text of company's Management Discussion and Analysis (MD&A) section from Form 10-Q and 10-K. 
# Output: Sentiment classified as either Positive or Negative along with the Sentiment confidence score in percentage
# 
# Code is written in Python and uses following libraries:
# 
# * PANDAS
# * NLTK
# * SKLEARN
# * RANDOM
# * STATISTICS
# * PICKLE
# 
# Inaddition to above, it uses following files:
# 
#     * lemur-stopwords.txt:File containing STOP words
#     * clasfuncdef.py:     Contains some of the custom functions and classes
#     * Negative terms.csv: Training file of Negative terms denoting Negative Sentiment
#     * Positive Terms.csv: Training file of Positive terms denoting Positive Sentiment
#     * TestNegative.txt:   Sample 10-K input file denoting Negative Sentiment. 
#     * TestPositive.txt:   Sample 10-K input file denoting Positive Sentiment. 
#     
# This report shall evaluate Sentiment accuracy using following classifiers and then use the classifier with highest accuracy percentage to evaluate the 10-K input.
# 
#     * Naive Bayes Classifier
#     * MultinomialNB Classifier
#     * BernoulliNB Classifier
#     * Logistic Regression Classifier
#     * SGD Classifier
#     * LinerSVC Classifier
# 
# This sentiment analysis report shall use file "lemur-stopwords.txt" to ignore the most common words. It also uses Lemmatizer. It is similar to a stemmer however, the output shall be a proper word from english dictionary. 
# 
# Concept of pickling has been used. Once the classifer's are trained to a desired accuracy, this program gives an option to save it under folder named "pickle". All subsequent execution of the report shall used the saved classifiers instead of evaluating them again. This shall help reduce the report execution time significantly. 
# Note: If we want to the report to re-evaluate without using the pickle concept, the files in the folder "pickle" needs to be deleted. Only if the file does not exist, system shall evaluate and save.

# In[55]:


import pandas as pd
import random
import clasfuncdef as cfd
import nltk
import pickle
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

exist_NB_classifier = ''
exist_MNB_classifier = ''
exist_BNB_classifier = ''
exist_LR_classifier  = ''
exist_SGD_classifier = ''
exist_LSVC_classifier = ''
exist_selected_classifier = ''


# In[56]:


print("Importing Positive Terms..")
positive_terms = open("Positive Terms.csv","r").read()
print("Import Positive Terms complete !!")

print("")
print("Importing Negative Terms..")
negative_terms = open("Negative Terms.csv","r").read()
print("Import Negative Terms complete !!")
print("")

# fname = 'TestPositive.txt'
# fname = 'TestNegative.txt'

print("Importing Comments whose sentiment shall be analysed..")
print("")
print("Enter TestPositive.txt to analyse a Positive sample")
print("Enter TestNegative.txt to analyse a Negative sample")
print("")

fname = input("Enter file name to analyze the sentiment: ")

print('File name to be read is:', fname)

try:
    src_comments = open(fname,"r").read()
except Exception as e:
    print('Unable to read the file !!')
    exit()


# Build Vocabulary and collect sample Positive, Negative terms:
# 
# It uses find_features function defined in the file clasfuncdef.py
# This function:
# * uses Lemmatizer instead of Stemming. This helps build tokens which are proper words.
# * Uses the lemur-stopwords.txt file to remove the stop words.
# * Builds the featureset to be used in the classifer.
# 
# Below is a snapshot of the function. 
# def find_features(features_list, term):
# 
#     lemmatizer = WordNetLemmatizer()
#     str = lemmatizer.lemmatize(term)
#     words = word_tokenize(str)
#     stop_words = open("lemur-stopwords.txt","r").read()
#     filtered_sentence = [w for w in words if not w in stop_words]
# 
#     features = {}
#     for w in features_list:
#         features[w] = (w in filtered_sentence)
# 
#     return features

# In[57]:


print('Building FeatureSet..')
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


# Split data into Training and Test. This shall be used in the classifer evalation. Classifers are trained using Train method and then tested for accuracy. 

# In[58]:


set_training = featuresets[:50]
set_testing =  featuresets[50:]


# Evaluate Naive Bayes Classifier (Read the Classifier from the Pickle folder if available):

# In[59]:


# NB_classifier = nltk.NaiveBayesClassifier.train(set_training)
try:
    open_file = open("pickle/save_NB_classifier.pickle", "rb")
    NB_classifier = pickle.load(open_file)
    open_file.close()
    exist_NB_classifier = 'X'
    print('File read from Pickle')
except Exception as e:
    print(e)
    NB_classifier = nltk.NaiveBayesClassifier.train(set_training)
    print('Saved classifier could not be found. It was evaluated')
    
print("Naive Bayes classifier accuracy %age:", (nltk.classify.accuracy(NB_classifier, set_testing))*100)
print('')


# Evaluate MultinomialNB Classifier (Read the Classifier from the Pickle folder if available):

# In[60]:


# MNB_classifier = SklearnClassifier(MultinomialNB())
# MNB_classifier.train(set_training)
try:
    open_file = open("pickle/save_MNB_classifier.pickle", "rb")
    MNB_classifier = pickle.load(open_file)
    open_file.close()
    exist_MNB_classifier = 'X'
    print('File read from Pickle')
except Exception as e:
    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(set_training)
    print('Saved classifier could not be found. It was evaluated')
    
print("MultinomialNB classifier accuracy %age:", (nltk.classify.accuracy(MNB_classifier, set_testing))*100)
print('')


# Evaluate BernoulliNB Classifier:

# In[61]:


# BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
# BernoulliNB_classifier.train(set_training)

try:
    open_file = open("pickle/save_BernoulliNB_classifier.pickle", "rb")
    BernoulliNB_classifier = pickle.load(open_file)
    open_file.close()
    exist_BNB_classifier = 'X'
    print('File read from Pickle')
except Exception as e:
    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier.train(set_training)
    print('Saved classifier could not be found. It was evaluated')
          
print("BernoulliNB classifier accuracy %age:", (nltk.classify.accuracy(BernoulliNB_classifier, set_testing))*100)
print('')


# Evaluate Logistic Regression Classifier:

# In[62]:


try:
    open_file = open("save_LogisticRegression_classifier.pickle", "rb")
    LogisticRegression_classifier = pickle.load(open_file)
    open_file.close()
    exist_LR_classifier = 'X'
    print('File read from Pickle')
except Exception as e:
    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(set_training)
    print('Saved classifier could not be found. It was evaluated')

print("LogisticRegression classifier accuracy %age:", (nltk.classify.accuracy(LogisticRegression_classifier, set_testing))*100)
print('')


# Evaluate SGD Classifier:

# In[63]:


try:
    open_file = open("save_SGDClassifier_classifier.pickle", "rb")
    SGDClassifier_classifier = pickle.load(open_file)
    open_file.close()
    exist_SGD_classifier = 'X'
    print('File read from Pickle')
except Exception as e:
    SGDClassifier_classifier = SklearnClassifier(SGDClassifier(max_iter=5, tol=None))
    SGDClassifier_classifier.train(set_training)
    print('Saved classifier could not be found. It was evaluated')


print("SGD classifier accuracy %age:", (nltk.classify.accuracy(SGDClassifier_classifier, set_testing))*100)
print('')


# Evaluate LinearSVC Classifier

# In[64]:


try:
    open_file = open("save_LinearSVC_classifier.pickle", "rb")
    LinearSVC_classifier = pickle.load(open_file)
    open_file.close()
    exist_LSVC_classifier = 'X'
    print('File read from Pickle')
except Exception as e:
    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(set_training)
    print('Saved classifier could not be found. It was evaluated')


print("LinearSVC classifier accuracy %age:", (nltk.classify.accuracy(LinearSVC_classifier, set_testing))*100)
print('')


# Compare the Classifiers and select the classifier with highest accuracy:
# selectclassifier is defined in the file clasfuncdef.py
# Below is a snapshot of the code:
# 
# Mode functionality returns an error whenever two classifiers return the same accuracy percentage. Inorder to overcome this issue, I have defined the custom find_max_mode  function.
# 
# def find_max_mode(list1):
#     list_table = statistics._counts(list1)
#     len_table = len(list_table)
# 
#     if len_table == 1:
#         max_mode = statistics.mode(list1)
#     else:
#         new_list = []
#         for i in range(len_table):
#             new_list.append(list_table[i][0])
#         max_mode = max(new_list)
#     return max_mode
# 
# class selectClassifier(ClassifierI):
#     def __init__(self, *classifiers):
#         self._classifiers = classifiers
# 
#     def classify(self, features):
#         votes = []
#         for x in self._classifiers:
#             v = x.classify(features)
#             votes.append(v)
#         return find_max_mode(votes)
# 
#     def confidence(self, features):
#         votes = []
#         for x in self._classifiers:
#             v = x.classify(features)
#             votes.append(v)
# 
#         choice_votes = votes.count(find_max_mode(votes))
#         conf = choice_votes / len(votes)
#         return conf

# In[65]:


try:
    open_file = open("save_selected_classifier.pickle", "rb")
    selected_classifier = pickle.load(open_file)
    open_file.close()
    exist_selected_classifier = 'X'
    print('File read from Pickle')
except Exception as e:
    selected_classifier = cfd.selectClassifier(
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)
    print('Saved classifier could not be found. It was evaluated')

print("Selected Classifier accuracy %age:", (nltk.classify.accuracy(selected_classifier, set_testing))*100)
print('')


# Save the trained classifiers in folder "PICKLE". This will help us avoid train the classifiers everytime we want to conduct sentiment analysis. It will help speed up the execution time. Here, system shall prompt user if they want to SAVE the data. If selected Yes, data shall be saved and any subsequent sentiment analysis shall be using the stored data rather than evaluating it again. 

# In[66]:


save_data = input('Enter Yes to SAVE the trained data')

if save_data.upper() == 'YES':
    print('Saving the data... Please wait !!')
    
    save_terms_collection = open("pickle/terms_collection.pickle","wb")
    pickle.dump(terms_collection, save_terms_collection)
    save_terms_collection.close()
    
    save_features_list = open("pickle/features_list.pickle","wb")
    pickle.dump(features_list, save_features_list)
    save_features_list.close()
    
    if exist_NB_classifier == '':
        save_NB_classifier = open("pickle/save_NB_classifier.pickle","wb")
        pickle.dump(NB_classifier, save_NB_classifier)
        save_NB_classifier.close()
    
    if exist_MNB_classifier == '':
        save_MNB_classifier = open("pickle/save_MNB_classifier.pickle","wb")
        pickle.dump(MNB_classifier, save_MNB_classifier)
        save_MNB_classifier.close() 
    
    if exist_BNB_classifier == '':
        save_BernoulliNB_classifier = open("pickle/save_BernoulliNB_classifier.pickle","wb")
        pickle.dump(BernoulliNB_classifier, save_BernoulliNB_classifier)
        save_BernoulliNB_classifier.close()
    
    if exist_LR_classifier == '':
        save_LogisticRegression_classifier = open("pickle/save_LogisticRegression_classifier.pickle","wb")
        pickle.dump(LogisticRegression_classifier, save_LogisticRegression_classifier)
        save_LogisticRegression_classifier.close()    
    
    if exist_SGD_classifier == '':
        save_SGDClassifier_classifier = open("pickle/save_SGDClassifier_classifier.pickle","wb")
        pickle.dump(SGDClassifier_classifier, save_SGDClassifier_classifier)
        save_SGDClassifier_classifier.close()
    
    if exist_LSVC_classifier == '':
        save_LinearSVC_classifier = open("pickle/save_LinearSVC_classifier.pickle","wb")
        pickle.dump(LinearSVC_classifier, save_LinearSVC_classifier)
        save_LinearSVC_classifier.close()     
    
    if exist_selected_classifier == '':
        save_selected_classifier = open("pickle/save_selected_classifier.pickle","wb")
        pickle.dump(selected_classifier, save_selected_classifier)
        save_selected_classifier.close()    
    
    print('Saving data complete !!')


# Now the Classifer is ready to evaluate the 10-K file. We will re-use the find features function defined above on the 10-K file to get the featureset.

# In[67]:


features_src_comments = cfd.find_features(features_list,src_comments)
print('')


# Evaluate the Sentiment (Positive/Negative) and the confidence score (in percentage)

# In[68]:


print('Sentiment: ', selected_classifier.classify(features_src_comments).upper())
print('Sentiment Confidence: ', selected_classifier.confidence(features_src_comments)*100, ' %age')


# In[ ]:




