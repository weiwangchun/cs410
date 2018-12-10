# CS410 UIUC - Download MDA reports from SEC EDGAR
# Python 3
# Wang Chun Wei / Venkat Rao
# Filter index to consist of only selected companies
# Output is an index of 10k 10q reports for a selected companies
# ----------------------------------------------------------------------------

import sys
import csv

# extract list of stocks that we will analyse
def get_selected_filings(stock_file, index_file):
    # stock_file:   list of stocks we will analyze
    # index_file:   list of all 10Q/10K filings

    stock_list = []
    with open(stock_file, 'r') as csv_file:
        stocks = csv.reader(csv_file, delimiter = ",")
        for row in stocks:
            stock_list.append(row)

    index_filings = []
    with open(index_file, 'r') as csv_file:
        filings = csv.reader(csv_file, delimiter = "|")
        for row in filings:
            index_filings.append(row)

    stock_list_cik = [x[0] for x in stock_list]

    selected_index_filings = []
    for filing in index_filings:
        if filing[0] in stock_list_cik:
            selected_index_filings.append(filing)

    return selected_index_filings


# extract stocks from the stock list that we have data for
def verify_stock_list(stock_file, selected_index_filings):

    stock_list = []
    with open(stock_file, 'r') as csv_file:
        stocks = csv.reader(csv_file, delimiter = ",")
        for row in stocks:
            stock_list.append(row)

    selected_index_cik = [x[0] for x in selected_index_filings]

    new_stock_list = []
    for stock in stock_list:
        if stock[0] in selected_index_cik:
            new_stock_list.append(stock)

    # write file
    file_out = open("successfully_fetched_stock_list.csv", 'w')
    for stock in new_stock_list:
        file_out.write(','.join(stock))
        file_out.write('\n')
    file_out.close()

    return new_stock_list


# print selected index filings
def print_selected_filings(selected_index_filings):
    result_index = 'index_files/selected_filings.idx'
    file_out = open(result_index, 'w') # open file 
    for filing in selected_index_filings:
        file_out.write(','.join(filing))
        file_out.write('\n')
    file_out.close()   

    return None


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Please provide stock_list and master_index_file. \nFor Example: >python filter_index.py stock_list_illinois.csv index_files/10X-2018-2018.idx \n")
        sys.exit(1)

    stock_file = str(sys.argv[1])
    index_file = str(sys.argv[2])

    selected_index_filings = get_selected_filings(stock_file, index_file)
    # generate new index with filings of stocks that we are interested in, based on stock_list
    print_selected_filings(selected_index_filings)
    # verify_stock_list(stock_file, selected_index_filings)



