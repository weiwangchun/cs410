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
    filing_list = []

    # open index file as csv file - go through each row
    with open(index_name, 'r') as csv_file:
        filings = csv.reader(csv_file, delimiter ="|")
        for row in filings:
            for item in row:
                filing_items += (item, )
            tmp = EDGAR_file(filing_items)

            # Save the MDA file
            tmp_file = open('files/' + tmp.cik + '_' + tmp.company_name + '_' + tmp.form_type + '_' +tmp.filing_date + '.txt','w')
            tmp_file.write(str(tmp.text_mda))
            tmp_file.close()

            #tmp.text_raw
            #filing_list.append(tmp)
            filing_items = ()
    #return filing_list
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
        trim_beginning = re.search(r'item[\s\w\&\.\;\,\:]*management[\s\']*s discussion and analysis', text, re.M | re.I) #ignore case 
        if trim_beginning:
            text = text[trim_beginning.end():]
            trim_end = re.search(r'item[\s\w\&\.\;\,\:]*quantitative and qualitative', text, re.M | re.I)
            if trim_end:
                # trim beginning and end complete
                print('MDA Trim Complete for ' + self.company_name + ' for ' + self.filing_date)
                text = text[:trim_end.end()]
                text = purge_stopwords(text.split())
                self.text_mda = text
            else: 
                # trim end is not complete
                print('MDA Trim Error: No Tail. Abort MDA for ' + self.company_name + ' for ' + self.filing_date)
                self.text_mda = None
        else:
            # trim beginning not complete
            print('MDA Trim Error: No Head. Abort MDA for ' + self.company_name + ' for ' + self.filing_date)
            self.text_mda = None


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
    if len(sys.argv) != 4:
        print("Please provide start_year, end_year and download_type arguments. \ndownload_type: all (download all), index (download index only), report (download filing reports only) \nFor Example: >python download_reports.py 2017 2018 all")
        sys.exit(1)
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])
    download_type = sys.argv[3] 

    if (download_type == "all" or download_type == "index"): 
        print("Downloading index files from " + str(start_year) + " to " + str(end_year))
        download_index(start_year, end_year)
        extract_from_index(start_year, end_year)

    if (download_type == "all" or download_type == "report"):
        # find available index files to do download
        index_files = glob.glob('10X*.idx')
        for file in index_files:
            print(file)
            extract_files_from_index(file)




