# Management Sentiment Analysis in Company SEC Filings

Final Project CS410, UIUC
- Wang Chun Wei (wcwei2)
- Venkat Rao Bhamidipathi (vrb3)

## Introduction

This projects extracts management discussion and analysis (MD&A) sections of text from corporate 10K and 10Q filings from the SEC EDGAR database.



## Demo 



## Code Files

The project is broken several files based on the steps involved conducting sentiment analysis on SEC filings.

### Downloading Index File from EDGAR

This python file extracts the quarterly master index files from EDGAR.
It then isolates the 10K and 10Q reports from the master index as saves it in a news index file. 
Finally, it cleans up existing master index files from the directory, as they get quite big.

For example, downloading the master index Q1 2017 to Q4 2018:
```
>python download_index.py  2017 2018
```

For example, downloading master index Q1 2018 to Q4 2018:
```
>python download_index.py  2018 2018
```

You can find resulting index file in `index_files/10X-yyyy-yyyy.idx`.

```
CIK|Company Name|Form Type|Date Filed|Filename
--------------------------------------------------------------------------------
100517|United Continental Holdings, Inc.|10-K|2017-02-23|edgar/data/100517/0001193125-17-054129.txt
1019737|NAVIGANT CONSULTING INC|10-K|2017-02-17|edgar/data/1019737/0001193125-17-047900.txt
1024725|TENNECO INC|10-K|2017-02-24|edgar/data/1024725/0001024725-17-000005.txt
1037976|JONES LANG LASALLE INC|10-K|2017-02-23|edgar/data/1037976/0001037976-17-000012.txt
10456|BAXTER INTERNATIONAL INC|10-K|2017-02-23|edgar/data/10456/0001564590-17-002240.txt
```
CIK are unique company identifiers used by the SEC. The index file also provides company name, date, form type and filename.


### Filtering Index File Based on a Stock List

The EDAGR indices provide us with filings of all the listed companies in the US. 
Running sentiment analysis on all the companies by downloading and reading through their annual (10K) and quarterly (10Q) reports will take a very long time.
The `filter_index.py` function provides users with the ability to narrow down the filings to selected filings based on a stock list.

In our example, we want to only look at Illinois based companies. This is saved in a file called `stock_list_illinois.csv`

The contents of the file are as follows:
```
CIK,Ticker,Name,Exchange,SIC,Business,Incorporated
--------------------------------------------------
1551152,ABBV,Abbvie Inc,NYSE,2834,IL,DE
1800,ABT,Abbott Laboratories,NYSE,2834,IL,IL
1529377,ACRE,Ares Commercial Real Estate Corp,NYSE,6798,IL,MD
```
The key fields we require are the CIK identifier and the Ticker.

To filter all the 10Q and 10K reports for ones that are based in Illinois, we would use:

```
>python filter_index.py stock_list_illinois.csv index_files/10X-2017-2018.idx
```



## Introduction

The project aims to extract management sentiment across large capitalization American firms (eg. Dow Jones Industial Average constituents or S&P 500 constituents), 
whose quarterly (10Q) and annual reports (10K) are available in SEC (US Securities and Exchange Commission) filings.
Using the 'manager discussion and analysis' section (MD&A) of these reports, we are able to analyze management sentiment across different firms and across time.

### SEC's EDGAR Database

The EDGAR (Electronic Data Gathering, Analysis, and Retrieval) database is managed by the SEC and contains
public disclosure data regarding company quarterly (10Q) and annual reports (10K) as well as substantial holdings notices,
and mutual fund disclosures.
We focus on the 10Q and 10K reports that outline the financial performance of the firm.
In particular, we focus on the management discussion and analysis (MD&A) section which is the most subjective section of these accounting reports.
Unlike financial statements, the MD&A section conatins valuable information on management's comments regarding the future of the business.

## Project Proposal Details

### Function

We aim to create a Python tool that allows users collect and analyze management sentiment for any input firm (or list of firms) that has SEC filings.

### Who will benefit from such tool?

We envisage this to be useful for portfolio managers or private investors who wish to keep track of management sentiment.
This will be helpful for investors that may not have the time to read through all the documents, but simply want a high level gauge on market wide and firm wide sentiment.

### Similar tools that exist

Websites such as Last10K and Whalewisdom have utilized the scraping and analysis of company SEC filings for investors, alerting them of significant changes in manager holding, significant changes in reported accounting figures and general report sentiment. 

Our tool is slightly different because:

* It focuses specifically on sentiment in the MD&A section.

* It allows users to analyse a large batch of stocks at once and compare and rank sentiment across stocks.


### Resources, Techniques and Algorithms used

We will use bag-of-words representation on the MD&A section.

For calculating sentiment, we will leverage off existing dictionaries and sentiment word lists in 
Loughran and McDonald (Journal of Finance, 2011) (https://sraf.nd.edu/textual-analysis/resources/).

This will allow us to measure sentiment categories in Loughran and McDonald: such as negative, postive, uncertainity, litigious, modal and constraining.

Further, we can use some machine learning classification algorithm to determine a final positive and negative prediction using the sentiment scores determined above. 

We will evaluate our tool by tabulating a confusion matrix and determining the accuracy of our classification algorithm.


## Steps and Deliverables

The activities required to complete the project is as follows:

- Aided by EDGAR's master index file, we can download the 10Q and 10K files of a given company name or ticker and date range.
- Extract the MD&A component from the 10Q and 10K files
- Conduct sentiment analysis on the MD&A sections using “Bag-of-words” approach
    * Input:  Name of the firm
    * Output: Sentiment score
      The process identifies positive and negative words (or a string of words) within an article. For this, it makes use of a large  dictionary which contains words that carry sentiment.  Each word in this dictionary can be assigned a weight. The sum of the positive and negative words is the final sentiment score generated by the model.


A rough timeline is provided below:

- Design: October 28th
- Development: November 18th
- Testing: December 1st

