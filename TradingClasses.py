import numpy as np
import pandas as pd
from datetime import datetime

from FunctionsForStats import *


# Configuration makes it easier to read more csvs. If a csv with different column names is given,
# this library might still be usable if the convig instance is changed.
# In the rest of the code, the config being used is called c.
class TradeCsvConfig:
    def __init__(self, date_format='20%y-%m-%d %H:%M:%S+00:00', clientid='clientId', symbol='symbol', time='time',
                 avgprice='avgPrice', currency='currency', botsld='BOT-SLD', bot='BOT', sld='SLD', shares='shares'):
        self.date_format = date_format
        self.clientid = clientid
        self.symbol = symbol
        self.time = time
        self.currency = currency
        self.botsld = botsld
        self.bot = bot
        self.sld = sld
        self.avgprice = avgprice
        self.shares = shares


# CompleteTrade takes as a constructor a data frame that has already been identified to meet these conditions:
# - The data frame is for one client for one symbol.
# - The data frame always has an open position, except for at the end, where there is not.
class CompleteTrade:
    def __init__(self, df, c):
        self.currency = df[c.currency].iloc[0]
        self.symbol = df[c.symbol].iloc[0]
        self.no_contracts = len(df)

        # treats the starting and end times as the first and last transactions.
        start = df[c.time].iloc[0]
        end = df[c.time].iloc[len(df) - 1]
        self.start_time = format_time(start, c) if isinstance(start, str) else start
        self.end_time = format_time(end, c) if isinstance(end, str) else end
        self.time_elapsed = self.end_time - self.start_time

        # calculates the profit by adding sells and subtracting buys, magnitude being shares * average price.
        self.profit = sum(df[c.shares] * df[c.avgprice] * [-1 if x == c.bot else 1 for x in df[c.botsld]])
        self.winning_trade = self.profit >= 0
        self.losing_trade = not self.winning_trade
        self.clientId = df[c.clientid].iloc[0]

    def __str__(self):
        sym = self.symbol
        prof = str(self.profit)
        cont = str(self.no_contracts)
        id = str(self.clientId)
        r = "\nClient/Symbol: " + id + "/" + sym + ", net: $" + prof + ", no. contracts: " + cont
        return r

    def __repr__(self):
        return self.__str__()


