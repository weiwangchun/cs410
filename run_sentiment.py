# CS410 UIUC - Run Sentiment Analysis
# Python 3
# Wang Chun Wei / Venkat Rao
# Run Basic Sentiment Analysis on \files\*.txt 
# ----------------------------------------------------------------------------


import glob
import pandas as pd
import metapy
import numpy as np
from itertools import chain





if __name__ == '__main__':

	# find MD&A files in the directory
    index_files = glob.glob('files/*.txt')
    for file in index_files:
        print(file)
        open_(file)




