import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import csv
import os


scriptHome = os.path.dirname(os.path.realpath(__file__))

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
    valid = True
    filename= ""

    def __init__(self, symbol):
        self.symbol = symbol
        self.filename = "{}.csv".format(symbol.replace(".","_").replace(" ","-"))
        self.ticker = yf.Ticker(self.symbol)

    def Fetch(self,data_period="5y",data_interval="1wk"):
        history_df = None

        dl_file = os.path.join(dl_folder,self.filename)
        bad_file = "{}.bad".format(dl_file[:-4])
        
        if os.path.exists(bad_file):
            self.valid = False
            return

        if os.path.exists(dl_file):
            print("Opening downloaded data for {}".format(self.symbol))
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

    def Plot(self,ax):
        if not self.valid:
            return
        close_df = self.history_df['Close']
        #close_df.columns = [self.symbol]
        ax.plot(close_df, label = self.symbol)

fig, ax = plt.subplots()

nSymbols = len(symbolList)
for num, symbol in enumerate(symbolList, start=1):
    print("Symbol {} of {}".format(num,nSymbols))
    stonk = Stonk(symbol)
    stonk.Fetch()
    stonk.Plot(ax)

leg = ax.legend()
ax.legend(loc='upper left', frameon=False)
plt.show()
