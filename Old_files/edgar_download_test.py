
# EDGAR 10Q and 10K download


# references: check out the below
# -----------------------------------------------
#https://github.com/edouardswiac/python-edgar
#https://github.com/Vaslo/CS410_Team32_FinalProj/blob/master/build_edgar_mda_files.py


import os
import io
import shutil
import sys
import csv
import re
import urllib.request 
import urllib.error
from bs4 import BeautifulSoup


# --------------------------------
# DOWNLOAD MASTER INDEX
# --------------------------------

# download index files from EDGAR
def download_index(start_year, end_year, URLstem):
    for year in range(start_year, end_year+1):
        for qtr in range(1, 5):
            currURL = URLstem + str(year) + '/QTR' + str(qtr) + '/master.idx'
            copy_file = str(year) + 'QTR' + str(qtr) + '.idx'
            local_file = 'master.idx'
            print('Downloading ' + str(year) + ' Q' + str(qtr) + ' master index.')

            try:
                response = urllib.request.urlopen(currURL)
                out_file = open(local_file, 'wb')
                shutil.copyfileobj(response, out_file)
                out_file.close()
                os.rename(local_file, copy_file)

            except urllib.error:
                print('URL not found.')


# --------------------------------
# EXTRACT 10K / 10Q INDEX
# --------------------------------

# extract 10Q and 10K from master idx
def extract_from_index(start_year, end_year):
    result_index = '10X-' + str(start_year) + '-' + str(end_year) + '.idx'
    file_out = open(result_index, 'w') # open file 
    for year in range(start_year, end_year+1):
        for qtr in range(1, 5):
            index_name = str(year) + 'QTR' + str(qtr) + '.idx'
            try:
                with io.open(index_name, 'r', encoding='latin-1') as file_in:
                    print('    ' + str(year) + ' Q' + str(qtr) + '... Found ' + str(extract10x(file_in, file_out)) + ' filings')
            except IOError:
                continue
    file_out.close()

# extract 10K and 10Q -- fix this function
def extract10x(index_file_handle, output_file_handle):

    count10x = 0
    for line in index_file_handle:
        if line.find('.txt') > 0:
            items = line.split('|')
            if items[2] in ('10-Q', '10-K'):
            #if items[2] == '10-Q':
                output_file_handle.write(line)
                count10x += 1
    return count10x



# --------------------------------
# DOWNLOAD FILES
# --------------------------------

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

            # also save the raw file - we probably don't need this later on - just good to have a look
            tmp_file = open('files/' + tmp.cik + tmp.company_name + tmp.filing_date + '.txt','w')
            tmp_file.write(str(tmp.text_clean))
            tmp_file.close()

            tmp.text_raw

            filing_list.append(tmp)
            filing_items = ()

    return filing_list








if __name__ == '__main__':

    start_year = 2018
    end_year = 2018
    URLstem = 'https://www.sec.gov/Archives/edgar/full-index/'

    # (1) download master index files
    #download_index(start_year, end_year, URLstem)

    # (2) build 10Q 10K index file
    #extract_from_index(start_year, end_year)

    # (3) extract files and clean txt
    extract_files_from_index('10X-2018-2018.idx')
