# CS410 UIUC - Download MDA reports from SEC EDGAR
# Python 3
# Wang Chun Wei / Venkat Rao
# Download 10K and 10Q Files from SEC EDGAR
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

# download master index files from EDGAR (quarterly files)
def download_index(start_year, end_year):
    for year in range(start_year, end_year + 1):
        for qtr in range(1, 5):
            idx_url = 'https://www.sec.gov/Archives/edgar/full-index/' + str(year) + '/QTR' + str(qtr) + '/master.idx'
            copy_filename = str(year) + 'QTR' + str(qtr) + '.idx'
            tmp_filename = 'master.idx'
            print('Downloading ' + str(year) + ' Q' + str(qtr) + ' master index.')
            try:
                response = urllib.request.urlopen(idx_url)
                out_file = open(tmp_filename, 'wb')
                shutil.copyfileobj(response, out_file)
                out_file.close()
                os.rename(tmp_filename, copy_filename)
            except urllib.error:
                print('Error: Cannot download master index. URL does not exist.')

# extract 10Q and 10K from master idx into new index 10X-yyyy-yyyy.idx
def extract_from_index(start_year, end_year):
    result_index = '10X-' + str(start_year) + '-' + str(end_year) + '.idx'
    file_out = open(result_index, 'w') # open file 
    for year in range(start_year, end_year+1):
        for qtr in range(1, 5):
            index_name = str(year) + 'QTR' + str(qtr) + '.idx'
            try:
                with io.open(index_name, 'r', encoding='latin-1') as file_in:
                    print('    ' + str(year) + ' Q' + str(qtr) + ' has ' + str(extract_reports(file_in, file_out)) + ' filings')
            except IOError:
                continue
    file_out.close()

# extract 10K and 10Q lines 
def extract_reports(index_file, output_file):
    counter = 0
    for line in index_file:
        if line.find('.txt') > 0:
            items = line.split('|')
            if items[2] in ('10-Q', '10-K'):
                output_file.write(line)
                counter  = counter + 1
    return counter

# download all EDGAR files listed in the index
def extract_files_from_index(index_name):
    filing_items = ()

    # open index file as csv file - go through each row
    with open(index_name, 'r') as csv_file:
        filings = csv.reader(csv_file, delimiter = "|")
        for row in filings:
            for item in row:
                filing_items += (item, )
            tmp = EDGAR_file(filing_items)

            # Save the MDA file
            tmp_file = open('files/' + tmp.cik + '_' + tmp.company_name + '_' + tmp.form_type + '_' +tmp.filing_date + '.txt','w')
            tmp_file.write(str(tmp.text_mda))
            tmp_file.close()

            filing_items = ()
    return None

# download all EDGAR files related to the specific stock_list
def extract_files_from_list(index_name, stock_list):
    filing_items = ()

    with open(index_name, 'r') as csv_file:
        filings = csv.reader(csv_file, delimiter = "|")
        for row in filings:
            # check if this row is relevant
            found = False
            for stock_str in stock_list:
                tmp = re.search(stock_str, ' '.join(row), re.M | re.I) 
                if tmp:
                    found = True
                    continue 
            # do only if relevant
            if found:
                for item in row:
                    filing_items += (item, )
                tmp = EDGAR_file(filing_items)

                # Save the MDA file
                tmp_file = open('files/' + tmp.cik + '_' + tmp.company_name + '_' + tmp.form_type + '_' +tmp.filing_date + '.txt','w')
                tmp_file.write(str(tmp.text_mda))
                tmp_file.close()

            filing_items = ()
    return None


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

    def get_file(self):
        #  get filing from SEC EDGAR database
        try:
            tmp = urllib.request.urlopen('http://www.sec.gov/Archives/' + self.filing_url)
            self.text_raw = tmp.read()
        except urllib.error:
            print('\t Error: No files found on SEC EDGAR database.')
            self.text_raw = ''

    def clean_text(self):
        # clean filing
        text = BeautifulSoup(self.text_raw, 'html.parser')
        self.text_clean = re.sub(r'[^\x00-\x7F]+|\W{2,}', ' ', text.document.get_text())

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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide json settings file.) \nFor Example: >python download_reports.py settings.json")
        sys.exit(1)
    settings_file = sys.argv[1]
    with open(settings_file) as f:
        settings = json.load(f)   
 
    download_type = settings['download_type']

    if (download_type == "all" or download_type == "index"): 
        print("Downloading index files from " + str(settings['start_year']) + " to " + str(settings['end_year']))
        download_index(settings['start_year'], settings['end_year'])
        extract_from_index(settings['start_year'], settings['end_year'])

    if (download_type == "all" or download_type == "report"):
        # find available index files to do download
        index_files = glob.glob('10X*.idx')
        for file in index_files:
            print(file)

            if (settings['stock_list']['use'] == "Y"):
                extract_files_from_list(file, settings['stock_list']['list'])
            else:
                extract_files_from_index(file)




