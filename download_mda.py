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


# download all EDGAR files listed in the index
def extract_files_from_index(index_name, start_from = 1):
    filing_items = ()

    # open index file as csv file - go through each row
    with open(index_name, 'r') as csv_file:
        filings = csv.reader(csv_file, delimiter = "|")
        counter = 1
        for row in filings:

            if counter >= start_from:
                for item in row:
                    filing_items += (item)

                tmp = EDGAR_file(filing_items)

                # Save the MDA file
                tmp_file = open('stock_files/mda_reports/' + tmp.cik + '_' + tmp.company_name + '_' + tmp.form_type + '_' +tmp.filing_date + '.txt','w')
                tmp_file.write(str(tmp.text_mda))
                tmp_file.close()

            filing_items = ()
            counter = counter + 1
    return None


# Remove stop words using the nltk package
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
    	tmp = CIK_TICKER_MAP[CIK_TICKER_MAP['CIK'] == self.cik]
    	self.ticker = tmp.Ticker[1]


    def clean_text(self):
        # clean filing
        text = BeautifulSoup(self.text_raw, 'html.parser')
        #text =[''.join(s.findAll(text=True))for s in soup.findAll('h1', 'time')]
        self.text_clean = re.sub(r'[^\x00-\x7F]+|\W{2,}', ' ', text.document.get_text())
        self.text_clean = re.sub('\n', ' ', self.text_clean)

    def extract_mda_section(self):
        # extract mda section from the clean filing
        text = self.text_clean
        trim_beginning = re.search(r'management[\s\']*s discussion and analysis', text, re.M | re.I) # this will pick up contents page
        if trim_beginning:
            text = text[trim_beginning.end():]
            trim_beginning = re.search(r'management[\s\']*s discussion and analysis', text, re.M | re.I) 
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
                self.text_mda = None
        else:
            # trim beginning not complete
            print('MDA Trim Error: No Head. Abort MDA for ' + self.company_name + ' for ' + self.filing_date)
            self.text_mda = None

    def clean_company_name(self):
        # make sure we can save company name as a filename
        self.company_name = re.sub('[!@#\/$]','', self.company_name)
        self.company_name = self.company_name.replace("\\","")

    def get_CAR(self):
    	# using self.ticker and EXCESSRET get cumulative abnormal returns
    	# check stock market reaction after 1 day and after 5 days
    	tmp = EXCESSRET[["Date", self.ticker]]
    	tmp = tmp[tmp["Date"] > self.filing_date]
    	self.CAR1 = tmp.iloc[0, 1]	# 1 day cumulative abnormal returns
    	self.CAR5 = sum(tmp.iloc[0:5, 1])	# 5 day cumulative abnormal returns
    	self.CAR10 = sum(tmp.iloc[0:10, 1])

    def run_BOW_sentiment(self):
    	# run bag of words (BOW) sentiment score











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


    # stock_files/ExcessRet_of_stock_file provides us with the excess returns 
    extract_files_from_index(selected_filings)


