# CS410 UIUC - Download Stock Prices
# Python 3
# Wang Chun Wei 
# Download Stock Prices using Wharton WRDS
# ----------------------------------------------------------------------------

## make sure you pip install pandas_datareader

import sys
import wrds
import csv
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web


# extract list of stocks that we will obtain prices for
def get_stock_list(stock_file):
    stock_list = []
    with open(stock_file, 'r') as csv_file:
        stocks = csv.reader(csv_file, delimiter = ",")
        for row in stocks:
            stock_list.append(row)
    return stock_list


# get stock prices via Yahoo - very slow - depreciated - use Wharton WRDS instead
def get_market_return(stock_list, start_date, end_date):
    # get matrix of stock prices
    for i in range(1,len(stock_list)):
        tmp_data = web.DataReader(stock_list[i][1], 'yahoo', start_date, end_date)
        tmp_data = tmp_data.reset_index()
        tmp_data = tmp_data[['Date', 'Adj Close']]   # take date and adjusted close price
        tmp_data.columns = ['Date', stock_list[i][0]] # use cik for columns

        if i == 1:
            prices = tmp_data
        else:
            prices  = pd.merge(prices, tmp_data, on ='Date')
    return prices


if __name__ == '__main__':

    stock_file = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]


    # use Wharton WRDS to get stock prices
    db = wrds.Connection()
    # grab stock names from the CRSP database
    stocknames = db.get_table(library='crsp', table = 'stocknames')
    stock_list = get_stock_list(stock_file)
    stock_list_ticker =  [x[1] for x in stock_list]

    # only grab stocknames that are in the stock_list
    selected_stocknames = [row for index, row in stocknames.iterrows() if (row.ticker in stock_list_ticker) & (str(row.nameenddt) == "2018-06-29")]

    # construct returns matrix
    counter = 0
    for stock in selected_stocknames:
        tmp = db.raw_sql("select date, ret from crsp.dsf where permno = " + str(stock.permno)  +  " and date > '" + start_date + "'")
        tmp.columns = ['Date', stock.ticker] # use cik for columns
        counter = counter + 1
        if counter == 1:
            returns = tmp
        else:
            returns  = pd.merge(returns, tmp, on ='Date')

    # get S&P Composite Return - proxy for index
    tmp = db.raw_sql("select date, sprtrn from crsp.dsi where date > '" + start_date + "'")
    tmp.columns = ['Date', 'Index'] # use cik for columns
    returns  = pd.merge(returns, tmp, on ='Date')

    # calculate excess returns
    excessret = returns
    stock_columns = [col for col in returns.columns if col not in ['Date', 'Index']]

    for stock in stock_columns:
        excessret[stock] = returns[stock] - returns.Index

    # save csv file
    excessret.to_csv('stock_files/ExcessRet_of_' + stock_file, index=False)
    returns.to_csv('stock_files/TotalRet_of_' + stock_file, index=False)


    # # write file
    # file_out = open("stock_list_available_in_crsp.csv", 'w')
    # for stock in selected_stocknames:
    #     file_out.write(','.join(stock[6:7]))
    #     file_out.write('\n')
    # file_out.close()