# CS410 UIUC - Download MDA reports from SEC EDGAR
# Python 3
# Wang Chun Wei / Venkat Rao
# Download MDA text from EDGAR
# Run bag of words sentiment analysis
# work out subsequent stock cumulative abnormal returns
# ----------------------------------------------------------------------------

import sys
import os
import io
import shutil
import urllib.request 
import urllib.error
import glob
import re
import csv
import json
from bs4 import BeautifulSoup
import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import pandas as pd
import numpy as np
import metapy
import pickle


# download all EDGAR files listed in the index
# returns a list of mda featues and classification
def extract_mda_from_index(index_name, start_from = 1, write_files = True):
    
    mda = []
    summary = []
    filing_items = ()

    # open index file as csv file - go through each row
    with open(index_name, 'r') as csv_file:
        filings = csv.reader(csv_file, delimiter = "|")
        counter = 1
        for row in filings:

            if counter >= start_from:
                for item in row:
                    filing_items += (item, )

                print(filing_items)    
                tmp = EDGAR_file(filing_items)

                mda.append((tmp.word_list, tmp.market_sentiment))
                summary.append((tmp.cik, tmp.ticker, tmp.company_name, tmp.rating, tmp.market_sentiment ))

                # Save the MDA file
                if write_files == True:
                    tmp_file = open('stock_files/mda_reports/' + tmp.cik + '_' + tmp.company_name + '_' + tmp.form_type + '_' +tmp.filing_date + '.txt','w')
                    tmp_file.write(str(tmp.text_mda))
                    tmp_file.close()

                    with open('stock_files/mda_reports/mda.pickle', 'wb') as f:
                        pickle.dump(mda, f)

            filing_items = ()
            counter = counter + 1

        if write_files == True:
            tmp_file = open('stock_files/' + 'summary.csv','w')
            for x in summary:
                tmp_file.write(','.join( x ))
                tmp_file.write('\n')
            tmp_file.close()         

    return mda
# use mda for classifer


# Remove stop words using the nltk package
# we use this the class EDGAR_file
def purge_stopwords(text):
    try:
        stop_words = stopwords.words('english')
    except:
        print('Download Stopwords from NLTK - this might take a while.\n')
        nltk.download('stopwords')
        stop_words = stopwords.words('english')

    filtered_text = [w for w in text if not w in stop_words] 
    return filtered_text


class EDGAR_file:
    text_raw = None
    text_clean = None
    text_mda = None
    rating = 'Neutral'
    market_sentiment ='Neutral'

    def __init__(self, filing_items):
        (self.cik,
        self.company_name,
        self.form_type,
        self.filing_date,
        self.filing_url) = filing_items
        self.filing_url = self.filing_url
        self.get_file()
        self.clean_company_name()
        self.clean_text()
        self.extract_mda_section()
        self.get_ticker()
        self.run_sentiment()
        self.get_CAR()
        

    def get_file(self):
        #  get filing from SEC EDGAR database
        try:
            tmp = urllib.request.urlopen('http://www.sec.gov/Archives/' + self.filing_url)
            self.text_raw = tmp.read()
        except urllib.error:
            print('\t Error: No files found on SEC EDGAR database.')
            self.text_raw = ''


    def get_ticker(self):
        # get ticker from cik using CIK_TICKER_MAP
        tmp = CIK_TICKER_MAP[CIK_TICKER_MAP['CIK'] == int(self.cik)]
        self.ticker = tmp.Ticker.iloc[0]


    def clean_text(self):
        # clean filing
        text = BeautifulSoup(self.text_raw, 'html.parser')
        #text =[''.join(s.findAll(text=True))for s in soup.findAll('h1', 'time')]
        self.text_clean = re.sub(r'[^\x00-\x7F]+|\W{2,}', ' ', text.document.get_text())
        self.text_clean = re.sub('\n', ' ', self.text_clean)
        self.text_clean = self.text_clean.replace('\\n','')

    def extract_mda_section(self):
        # extract mda section from the clean filing
        text = self.text_clean
        #trim_beginning = re.search(r'management[\s\']*s discussion and analysis', text, re.M | re.I) # this will pick up contents page
        trim_beginning = re.search(r'discussion and analysis of financial', text, re.M | re.I)
        if trim_beginning:
            text = text[trim_beginning.end():]
            #trim_beginning = re.search(r'management[\s\']*s discussion and analysis', text, re.M | re.I) 
            trim_beginning = re.search(r'discussion and analysis of financial', text, re.M | re.I)
            if trim_beginning:
                text = text[trim_beginning.end():]
            trim_end = re.search(r'quantitative and qualitative', text, re.M | re.I)
            if trim_end:
                # trim beginning and end complete
                print('MDA Trim Complete for ' + self.company_name + ' for ' + self.filing_date)
                text = text[:trim_end.end()]
                text = purge_stopwords(text.split())
                self.text_mda = ' '.join(text)
            else: 
                # trim end is not complete
                print('MDA Trim Error: No Tail. Abort MDA for ' + self.company_name + ' for ' + self.filing_date)
                self.text_mda = text
                tmp_file = open('stock_files/mda_reports/error_' + self.cik + '_' + self.company_name + '_' + self.form_type + '_' + self.filing_date + '.txt','w')
                tmp_file.write(str(self.text_raw))
                tmp_file.close()

        else:
            # trim beginning not complete
            print('MDA Trim Error: No Head. Abort MDA for ' + self.company_name + ' for ' + self.filing_date)
            self.text_mda = 'Neutral Text'
            tmp_file = open('stock_files/mda_reports/error_' + self.cik + '_' + self.company_name + '_' + self.form_type + '_' + self.filing_date + '.txt','w')
            tmp_file.write(str(self.text_raw))
            tmp_file.close()

    def clean_company_name(self):
        # make sure we can save company name as a filename
        self.company_name = re.sub('[!@#\/$]','', self.company_name)
        self.company_name = self.company_name.replace("\\","")

    def get_CAR(self):
        # using self.ticker and EXCESSRET get cumulative abnormal returns
        # check stock market reaction after 1 day and after 5 days
        try: 
            tmp = EXCESSRET[["Date", self.ticker]]
            tmp = tmp[tmp["Date"] > self.filing_date]
            self.CAR1 = tmp.iloc[0, 1]  # 1 day cumulative abnormal returns
            self.CAR5 = sum(tmp.iloc[0:5, 1])   # 5 day cumulative abnormal returns
            self.CAR10 = sum(tmp.iloc[0:10, 1])
            # let us use CAR5 to be market setiment
            if (self.CAR5 > 0):
                self.market_sentiment= 'Positive'
            else:
                self.market_sentiment= 'Negative'
        except:
            print("CAR was not found!\n")
            self.market_sentiment = self.rating # if car not available, use BOW sentiment
        return None


    def tokenize(self):
        # get word list for self.text_mda
        word_list= []
        doc = metapy.index.Document()
        doc.content(self.text_mda)
        tok= metapy.analyzers.ICUTokenizer()
        tok= metapy.analyzers.LowercaseFilter(tok)
        tok = metapy.analyzers.LengthFilter(tok, min=2, max=30)
        tok.set_content(doc.content())
        tokens = [word_list.append(token.upper()) for token in tok]
        self.word_list = word_list


    def run_sentiment(self):
        # run bag of words sentiment score

        self.tokenize()
        # get sentiment rating:  - in the future consider "uncertainty", "litigious", "superfluous" and other dimensions
        matches = MASTER_DICT.loc[MASTER_DICT['Word'].isin(self.word_list)]
        negative_words = matches.loc[matches['Negative']!=0]['Word']
        positive_words = matches.loc[matches['Positive']!=0]['Word']
        negative_matches = np.sum(matches['Negative'] !=0)
        positive_matches = np.sum(matches['Positive'] !=0)
        if (negative_matches <= positive_matches):
            self.rating= 'Positive'
        else:
            self.rating= 'Negative'
        return None



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Please provide filing index file and stock_list file. \nFor Example: >python download_mda.py index_files/selected_filings.idx stock_list_illinois.csv")
        sys.exit(1)

    selected_filings = sys.argv[1]
    stock_file = sys.argv[2]

    # stock_file maps cik to ticker
    CIK_TICKER_MAP = pd.read_csv(stock_file)
    # stock excess returns
    EXCESSRET = pd.read_csv('stock_files/ExcessRet_of_' + stock_file)
    # downloard master dictionary
    MASTER_DICT = pd.read_excel("master_dictionary.xlsx")


    # stock_files/ExcessRet_of_stock_file provides us with the excess returns 
    mda = extract_mda_from_index(selected_filings, start_from = 120)



    # Note: when break run, make sure change pickle name - join later for sentiment analysis
