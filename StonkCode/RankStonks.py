print("Importing dependencies...")

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import csv
import os
import datetime
from Stonks import Stonk

in_data = r"output_data\CloseStats.csv"
out_data = r"output_data\RankedStonks.csv"

stats_df = pd.read_csv(in_data, header = 0, encoding = "ISO-8859-1")

results_df = pd.DataFrame(dtype="float64")

results_df['symbol'] = stats_df['Unnamed: 0']

results_df["long_direction"]=stats_df["75%_lastMonth"]/stats_df["75%_2019"]
results_df["short_direction"]=stats_df["25%_lastMonth"]/stats_df["75%_last2Months"]
results_df["current_vs_long"]=stats_df["last_close"]/stats_df["75%_2019"]
results_df["std_last2Months"]=stats_df["std_last2Months"]
results_df["rank"]=results_df["short_direction"]*results_df["short_direction"]/(results_df["current_vs_long"]*results_df["long_direction"])
results_df.sort_values(["rank"],inplace=True, ascending=False)
results_df.to_csv(out_data)