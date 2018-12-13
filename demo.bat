@echo off
echo '###################################################################################################'
echo 'Requires Python 3'
echo 'DEAR EXAMINER: If python is not recognized error occurs, the directory needs to be specified.'
echo 'For me it was: "C:\ProgramData\Anacondas3\python download_index.py 2018 2018" instead of simply "python download_index.py 2018 2018"'
echo '###################################################################################################'

echo 'Downloading Index Files from SEC EDGAR'
@echo on
python download_index.py 2018 2018
pause
python filter_index.py stock_list_illinois.csv index_files/10X-2018-2018.idx 

@echo off
echo '###################################################################################################'
echo 'Downloading MDA files....'

@echo on
python download_mda.py index_files/test_selected_filings.idx stock_list_illinois.csv
pause

@echo off
echo '###################################################################################################'
echo 'Run sentiment analysis on existing downloaded mda files in mda_illinois.pickle'
@echo on
python run_sentiment.py mda.pickle 0.80
pause
