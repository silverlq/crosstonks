print("Importing dependencies...")

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import csv
import os
import datetime

print("Loading potential symbols")

scriptHome = os.path.dirname(os.path.realpath(__file__))
potentialCsv = "potentialSymbols.csv"
dl_foldername = "downloaded_data"
dl_folder = os.path.join(scriptHome,dl_foldername)
if not os.path.exists(dl_folder):
    os.makedirs(dl_folder)

symbolFilepath = os.path.join(scriptHome,"ticker_symbols.csv")

symbol_df = pd.read_csv(symbolFilepath, header = 0, encoding = "ISO-8859-1")

symbolList = symbol_df.iloc[:,0].tolist()

class Stonk:
    ticker = None
    symbol = ""
    history_df = None
    close_df = None
    valid = True
    filename= ""
    potential = False
    stats = None

    def __init__(self, symbol):
        self.symbol = symbol
        self.filename = "{}.csv".format(symbol.replace(".","_").replace(" ","-"))
        self.ticker = yf.Ticker(self.symbol)
        self.stats = pd.Series(dtype="float64")

    def Fetch(self,data_period="5y",data_interval="1wk"):
        history_df = None

        dl_file = os.path.join(dl_folder,self.filename)
        bad_file = "{}.bad".format(dl_file[:-4])
        
        if os.path.exists(bad_file):
            self.valid = False
            return

        if os.path.exists(dl_file):
            #print("Opening downloaded data for {}".format(self.symbol))
            history_df = pd.read_csv(dl_file, index_col = 0, parse_dates = True)
            
        else:
            print("Fetching historical data for {}".format(self.symbol))
            history_df = self.ticker.history(period=data_period,interval=data_interval)

        if (history_df.empty or history_df.size <= 0):
            self.valid = False
            with open(bad_file,'w') as writer:
                writer.write("/n")
        else:
            self.history_df = history_df
            if not os.path.exists(dl_file):
                self.history_df.to_csv(dl_file)

    def Setup(self):
        if not self.valid:
            return

        self.close_df = self.history_df['Close']
        if "2019" not in self.close_df:
            self.valid = False
            return
        precovid_close = self.close_df["2019"]
        if (precovid_close.empty):
            self.valid = False
            return

        precovid_stats = precovid_close.describe()
        precovid_stats.index = ["2019_{}".format(x) for x in precovid_stats.index]
        
        monthAgo = str(datetime.date.today() - datetime.timedelta(days=60))
        lastMonth_stats = self.close_df[monthAgo:].describe()
        lastMonth_stats.index = ["last2Months_{}".format(x) for x in lastMonth_stats.index]

        last_close = pd.Series([self.close_df[-1]], index=['last_close'])

        self.stats

        self.stats = self.stats.append(precovid_stats)
        self.stats = self.stats.append(lastMonth_stats)
        self.stats = self.stats.append(last_close)

        #self.potential = (self.stats['last_close'] < self.stats['25%'] and self.stats['last_close'] < self.stats['75%']/2)

    def Plot(self,ax):
        if not self.valid or not self.potential:
            return
        
        #close_df.columns = [self.symbol]
        ax.plot(self.close_df, label = self.symbol)


print("Loading symbol historical data...")
fig, ax = plt.subplots()
potentialDict = {}
nSymbols = len(symbolList)
percent = 0
for num, symbol in enumerate(symbolList, start=1):
    new_percent = int(100*num/nSymbols)
    if(new_percent > percent):
        print("Loaded {:0>2d}% symbols of {}".format(new_percent,nSymbols))
    percent = new_percent
    stonk = Stonk(symbol)
    stonk.Fetch()
    stonk.Setup()
    #if stonk.potential:
    if stonk.valid and not stonk.stats.empty:
        potentialDict[stonk.symbol]=stonk.stats.T
        #stonk.Plot(ax)
    #if num > 20:
    #    break

potential_df = pd.concat(potentialDict,axis=1)
potential_df.T.to_csv(os.path.join(scriptHome,potentialCsv))

leg = ax.legend()
ax.legend(loc='upper left', frameon=False)
plt.show()
