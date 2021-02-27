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

out_folder= Folder(r"output_data")
in_folder= Folder(r"output_data\stonk_close")

symbolFilepath = os.path.join(scriptHome,"ticker_symbols.csv")

symbol_df = pd.read_csv(symbolFilepath, header = 0, encoding = "ISO-8859-1")

symbolList = symbol_df.iloc[:,0].tolist()

print("Loading symbol close data...")
fig, ax = plt.subplots()


lastMonth = datetime.date.today() - datetime.timedelta(days=30)
last2months = lastMonth - datetime.timedelta(days=30)

statsDict = {}

nSymbols = len(symbolList)
percent = 0
for num, symbol in enumerate(symbolList, start=1):
    new_percent = int(100*num/nSymbols)
    if(new_percent > percent):
        print("Loaded {:0>2d}% symbols of {}".format(new_percent,nSymbols))
    percent = new_percent
    stonk = Stonk(symbol)
    stonk.LoadCloseHist(in_folder)
    
    if stonk.valid and "2019" in stonk.close_df and "2021" in stonk.close_df:
        stats =  pd.Series(dtype="float64")
        close_2019 = stonk.close_df["2019"].describe()
        close_2019.index = ["{}_2019".format(x) for x in close_2019.index]

        close_last2months = stonk.close_df[str(last2months):].describe()
        close_last2months.index = ["{}_last2Months".format(x) for x in close_last2months.index]

        close_lastMonth = stonk.close_df[str(lastMonth):].describe()
        close_lastMonth.index = ["{}_lastMonth".format(x) for x in close_lastMonth.index]

        last_close = pd.Series([stonk.close_df[-1]], index=['last_close'])

        stats = stats.append(close_2019)
        stats = stats.append(close_last2months)
        stats = stats.append(close_lastMonth)
        stats = stats.append(last_close)
        
        statsDict[stonk.symbol]=stats

    #if num > 50:
    #    break
    
stats_df = pd.concat(statsDict,axis=1).T
stats_df.to_csv(os.path.join(out_folder,"CloseStats.csv"))