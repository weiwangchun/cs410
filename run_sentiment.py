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



class SentimentAnalysis:
	text  = None


	def __init__(self, file_name):
		self.file_name = file_name
		self.get_text()


	def get_text(self):
		



if __name__ == '__main__':

	# find MD&A files in the directory
    index_files = glob.glob('files/*.txt')
    for file in index_files:
        print(file)
        tmp = SentimentAnalysis(file)






