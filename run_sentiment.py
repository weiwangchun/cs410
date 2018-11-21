# CS410 UIUC - Run Sentiment Analysis
# Python 3
# Wang Chun Wei / Venkat Rao
# Run Basic Sentiment Analysis on \files\*.txt 
# ----------------------------------------------------------------------------


import glob
import csv
import pandas as pd
import metapy
import numpy as np
from itertools import chain


def get_m_2_ngrams(input_list, min, max):
    for s in chain(*[get_ngrams(input_list, k) for k in range(min, max+1)]):
        yield ' '.join(s)

def get_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])



class SentimentAnalysis:
    text = None
    score = None

    def __init__(self, file_name):
        self.file_name = file_name
        self.get_text()

    def get_text(self):
        # get text from directory
        file = open(self.file_name)
        self.text = file.read()


    def get_score(self):
        with open(self.file_name) as query_file:
            g_tokens = []
            strip_list = []
            bow = []
            for line in query_file:
                g_tokens.extend(line.split())

            for s in get_m_2_ngrams(g_tokens, 1, 6):
                bow.append(s)

        bow_df = pd.DataFrame(np.array(bow))
        bow_df.columns = ['Tokens']
        bow_df['count'] = bow_df.groupby('Tokens')['Tokens'].transform('count')

        values = bow_df['Tokens']
        pt['Match'] = pt['Positive'].isin(values).astype(int)
        nt['Match'] = nt['Negative'].isin(values).astype(int)

        positive_score = pt['Match'].sum()
        negative_score = nt['Match'].sum()

        sentiment = positive_score - negative_score
        self.score = sentiment


if __name__ == '__main__':

    # get positive words and negative words
    pt = pd.read_csv("Positive Terms.csv", encoding='latin1')
    nt = pd.read_csv("Negative Terms.csv", encoding='latin1')



    # find MD&A files in the directory
    index_files = glob.glob('files/*.txt')
    for file in index_files:
        print(file)
        tmp = SentimentAnalysis(file)







