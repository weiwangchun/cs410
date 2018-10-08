# CS410 Project Proposal: Management Sentiment Analysis in SEC Filings

The project aims to extract management sentiment across large capitalization American firms (eg. Dow Jones Industial Average constituents or S&P 500 constituents), 
whose quarterly (10Q) and annual reports (10K) are available in SEC (US Securities and Exchange Commission) filings.
Using the `manager discussion and analysis' section (MD&A) of these reports, we are able to analyze management sentiment across different firms and across time.
We can also correlate this to stock price performance to see if there are any linkages between implicit management sentiment and future stock price
performance.

We aim to create a Python tool that allows users collect and analyze management sentiment for any input firm that has SEC filings.
We envisage this to be useful for portfolio managers or private investors who wish to keep track of management sentiment.

## Team Members

- Venkat Rao Bhamidipathi (vrb3)
- Wang Chun Wei (wcwei2)


## SEC's EDGAR Database

The EDGAR (Electronic Data Gathering, Analysis, and Retrieval) database is managed by the SEC and contains
public disclosure data regarding company quarterly (10Q) and annual reports (10K) as well as substantial holdings notices,
and mutual fund disclosures.
We focus on the 10Q and 10K reports that outline the financial performance of the firm.
In particular, we focus on the management discussion and analysis (MD&A) section which is the most subjective section of these accounting reports.
Unlike financial statements, the MD&A section conatins valuable information on management's comments regarding the future of the business.

## Steps and Deliverables

The activities required to complete the project is as follows:

- Aided by EDGAR's master index file, we can download the 10Q and 10K files of a given company name or ticker and date range.
- Extract the MD&A component from the 10Q and 10K files
- Conduct sentiment analysis on the MD&A sections
