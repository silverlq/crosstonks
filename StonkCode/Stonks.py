import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import csv
import os
import datetime

class Stonk:
    symbol = ""
    history_df = None
    close_df = None
    valid = True
    filename= ""
    stats = None

    def __init__(self, symbol):
        self.symbol = symbol
        self.filename = "{}.csv".format(symbol.replace(".","_").replace(" ","-"))
        self.stats = pd.Series(dtype="float64")

    def Fetch(self,dl_folder="downloaded_data",data_period="5y",data_interval="1wk"):
        ticker = yf.Ticker(self.symbol)
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
            history_df = ticker.history(period=data_period,interval=data_interval)

        if (history_df.empty or history_df.size <= 0):
            self.valid = False
            with open(bad_file,'w') as writer:
                writer.write("/n")
        else:
            self.history_df = history_df
            if not os.path.exists(dl_file):
                self.history_df.to_csv(dl_file)

    def SaveCloseHist(self, out_folder = r"output_data\stonk_close"):
        if not self.valid:
            return
        self.close_df = self.history_df['Close']
        out_file = os.path.join(out_folder,self.filename)
        self.close_df.to_csv(out_file)

    def LoadCloseHist(self, in_folder = r"output_data\stonk_close"):
        in_file = os.path.join(in_folder,self.filename)
        if os.path.exists(in_file):
            self.close_df = pd.read_csv(in_file, index_col = 0, parse_dates = True, squeeze=True)
        else:
            self.valid = False
    def PrintInfo(self):
        ticker = yf.Ticker(self.symbol)
        info = ticker.info
        print("{} ({:.2f} {}) | {}\n{}\n\n{}\n\n{}\n\n\n".format(
            self.symbol,
            self.close_df[-1],
            info.get("currency"),
            info.get('longName'),
            info.get('sector'),
            info.get('website'),
            info.get('longBusinessSummary')))
    def Plot(self,ax=None):
        if not self.valid:
            return
        if ax is None:
            plt.plot(self.close_df)
        else:
            #close_df.columns = [self.symbol]
            ax.plot(self.close_df, label = self.symbol)

