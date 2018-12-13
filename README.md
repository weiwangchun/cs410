# Management Sentiment Analysis in Company SEC Filings

Final Project CS410, UIUC
- Wang Chun Wei (wcwei2)
- Venkat Rao Bhamidipathi (vrb3)

## Introduction

This projects extracts management discussion and analysis (MD&A) sections of text from corporate 10K and 10Q filings from the EDGAR database.
The EDGAR (Electronic Data Gathering, Analysis, and Retrieval) database is managed by the SEC and contains
public disclosure data regarding company quarterly (10Q) and annual reports (10K) as well as substantial holdings notices,
and mutual fund disclosures. We focus on the 10Q and 10K reports because they outline the financial performance of the firm.
In particular, we focus on the management discussion and analysis (MD&A) section which is the most subjective section of these accounting reports.
Unlike financial statements, the MD&A section conatins valuable information on management's comments regarding the future of the business.



## Demo 



## Code Files

The project is broken several files based on the steps involved conducting sentiment analysis on SEC filings.

### 1. Downloading Index File from EDGAR with `download_index.py`

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


### 2. Filtering Index File Based on a Stock List with `filter_index.py`

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

The resulting file will be saved as 'index_files/selected_filings.idx'


### 3. Downloading Returns with `download_prices.py` 

Since the end goal is to run sentiment analysis to predict stock market reactions to filing reports, we need to know the subsequent stock market price associated with the report announcement.
`download_prices.py` is to download total returns and excess returns over the index for a given stock list.

To get total and excess returns for all IL based firms from 1st Jan 2017 to 1st Dec 2018 would be as follows: 
```
>python download_prices.py stock_list_illinois.csv '2017-01-01' '2018-12-01'
```
Excess returns is used to calculate cumulative abnormal returns (CAR). https://en.wikipedia.org/wiki/Abnormal_return
This is used to determine market reaction to an event (10K or 10Q annoucement).

Note: This function requires users to have a Wharton WRDS account (https://wrds-web.wharton.upenn.edu/wrds/), as the data is pulled for there. It also uses the `wrds` Python package.
For testers / users with no WRDS account, in the `stock_files` folder, we have already downloaded the returns data for Illinois based stocks, so you can continue.


### 4. Extracting MD&A section using `download_mda.py`

Once we the have `selected_filings.idx` from step 2, we can go and download the reports. 
Since the reports are in html format, we use a html parser in beautifulsoup.
We then clean the text, removing any remaining  `\n` and then we isolate the MD&A (manager discussion and analysis) section of the filing.
We only keep the MD&A section. This is achieved by using `re.search` to find the string `discussion and analysis of financial`.
As these reports are fairly standardized, the 2nd occurance of this string pattern usually begins the MD&A section (the 1st occurance is in the contents page).
The MD&A section ends when the report begins to talk about 	`quantitative and qualitative` risk factors.
Generally this works well in isolating the MD&A section, although the accuracy is circa 90%.
Once we obtain the MD&A text, we tokenize and run bag-of-words sentiment based on the master dictionary provided by Loughran McDonald Financial Dictionary https://sraf.nd.edu/textual-analysis/.
Using the filing date, we also run sentiment based on cumulative abnormal returns (CAR) of the stock after filing date.
We argue that if the MD&A section is upbeat and positive, the cumulative abormal returns (CAR) in the market should be positive too and vice versa.
Our `true` sentiment score is based on a 5 day CAR, i.e. this is what we're trying to predict in our model.

We save a list of tokenized MD&As and their respective sentiment (positive or negative) based on market reaction (5 day CAR). This is saved in `stock_files/mda_reports/mda.pickle`.

To run our selected filings based on our Illinois stocks, we would do the following. We specify the index file and the stock_list file.

```
>python download_mda.py index_files/selected_filings.idx stock_list_illinois.csv
```

The results from this is actually saved in `mda_illinois.pickle`. This pickle contains the data to train and test our sentiment classifiers.
You can open pickle to have a look at the list

```
    with open('stock_files/mda_reports/mda_illinois.pickle','rb') as f:
        mda = pickle.load(f)
```

We have collected 445 MD&As and their respective stock market reactions. (Ideally we would like to run is for a lot more observations, but 445 still illustrates the point.)


### 5. Run sentiment using `run_sentiment.py`

Now we can run sentiment analysis using 6 different types of classifiers (Naive Bayes, Multinomial Naive Bayes, Bernoulli Naive Bayes, Losistic Regression, Stochastic Gradient Descent, Linear SVC) from the nltk package in Python.



For instance, 
```
 >python run_sentiment.py mda.pickle 0.80
```

