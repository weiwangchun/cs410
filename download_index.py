
# CS410 UIUC - Download MDA reports from SEC EDGAR
# Python 3
# Wang Chun Wei / Venkat Rao
# Download 10K and 10Q Indexes from SEC EDGAR
# ----------------------------------------------------------------------------



import sys
import os
import io
import shutil
import urllib.request 
import urllib.error



# download master index files from EDGAR (quarterly files)
def download_index(start_year, end_year):
    tmp_filename = 'index_files/master.idx'

    for year in range(start_year, end_year + 1):
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)

        for qtr in range(1, 5):
            idx_url = 'https://www.sec.gov/Archives/edgar/full-index/' + str(year) + '/QTR' + str(qtr) + '/master.idx'
            copy_filename = 'index_files/' + str(year) + 'QTR' + str(qtr) + '.idx'
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
    result_index = 'index_files/10X-' + str(start_year) + '-' + str(end_year) + '.idx'
    file_out = open(result_index, 'w') # open file 
    for year in range(start_year, end_year + 1):
        for qtr in range(1, 5):
            index_name = 'index_files/' + str(year) + 'QTR' + str(qtr) + '.idx'
            try:
                with io.open(index_name, 'r', encoding='latin-1') as file_in:
                    print('    ' + str(year) + ' Q' + str(qtr) + ' has ' + str(extract_reports_10k10q(file_in, file_out)) + ' filings')
            except IOError:
                continue
    file_out.close()

# extract 10K and 10Q filings 
def extract_reports_10k10q(index_file, output_file):
    counter = 0
    for line in index_file:
        if line.find('.txt') > 0:
            items = line.split('|')
            if items[2] in ('10-Q', '10-K'):
                output_file.write(line)
                counter  = counter + 1
    return counter

# extract 13F filings
def extract_reports_13f(index_file, output_file):
    counter = 0
    for line in index_file:
        if line.find('.txt') > 0:
            items = line.split('|')
            if items[2] in ('13F', '13F-HR'):
                output_file.write(line)
                counter  = counter + 1
    return counter

# clean up
# we only need 10X files - delete the master index files as they can get quite big
def clean_up(start_year, end_year):
    for year in range(start_year, end_year + 1):
        for qtr in range(1, 5):
            del_filename = 'index_files/' + str(year) + 'QTR' + str(qtr) + '.idx'

            if os.path.exists(del_filename):
                os.remove(del_filename)
            else:
                print(del_filename + " does not exist.")

    return None



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Please provide start_year and end_year where start_year <= end_year \nFor Example: >python download_index.py  2018 2018")
        sys.exit(1)

    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    print("Downloading index files from Q1 " + str(start_year) + " to Q4 " + str(end_year) + "\nSaved in folder index_files\n")
    download_index(start_year, end_year)
    extract_from_index(start_year, end_year)
    clean_up(start_year, end_year)

