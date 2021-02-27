print("Importing dependencies...")

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import csv
import os
import datetime
from Stonks import Stonk

in_data = r"output_data\RankedStonks.csv"

stats_df = pd.read_csv(in_data, header = 0, encoding = "ISO-8859-1")

symbolList = stats_df['symbol'].tolist()

#fig, ax = plt.subplots()
for num, symbol in enumerate(symbolList, start=1):
    stonk = Stonk(symbol)
    stonk.LoadCloseHist()
    
    if stonk.valid:
        try:
            stonk.PrintInfo()
            stonk.Plot()
            plt.show()
        except:
            print("Skipping {}...".format(stonk.symbol))
    if num > 100:
        break

#leg = ax.legend()
#ax.legend(loc='upper left', frameon=False)
#plt.show()