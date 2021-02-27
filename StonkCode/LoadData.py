print("Importing dependencies...")

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import csv
import os
import datetime
from Stonks import Stonk

print("Loading potential symbols")

scriptHome = os.path.dirname(os.path.realpath(__file__))

def Folder(f_name):
    f_path = os.path.join(scriptHome,f_name)
    if not os.path.exists(f_path):
        os.makedirs(f_path)
    return f_path

out_folder= Folder(r"output_data\stonk_close")
dl_folder = Folder("downloaded_data")
outCsv = "stonksClose.csv"

symbolFilepath = os.path.join(scriptHome,"ticker_symbols.csv")

symbol_df = pd.read_csv(symbolFilepath, header = 0, encoding = "ISO-8859-1")

symbolList = symbol_df.iloc[:,0].tolist()

print("Loading symbol historical data...")
fig, ax = plt.subplots()

nSymbols = len(symbolList)
percent = 0
for num, symbol in enumerate(symbolList, start=1):
    new_percent = int(100*num/nSymbols)
    if(new_percent > percent):
        print("Loaded {:0>2d}% symbols of {}".format(new_percent,nSymbols))
    percent = new_percent
    stonk = Stonk(symbol)
    stonk.Fetch(data_interval='1d')
    
    if stonk.valid:
        stonk.SaveCloseHist()

    #if num > 200:
    #    break
    