import numpy as np
import pandas as pd
from datetime import datetime

data = pd.read_csv("order_details_US2.csv")


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


# This only works assuming the time-zone traded in is +00:00, for now.
def format_time(time, c):
    return datetime.strptime(time, c.date_format)


# filters a list for either winning trades or losing trades.
def trade_filter(trades, winning):
    return list(filter(lambda x: x.winning_trade if winning else x.losing_trade, trades))


# I'm not sure if something like this is already built into python syntax - I suspect it is. But just in case:
def get_list(trades, want):
    if want == 'symbol':
        return [x.symbol for x in trades]
    elif want == 'currency':
        return [x.currency for x in trades]
    elif want == 'no_contracts':
        return [x.no_contracts for x in trades]
    elif want == 'time_elapsed':
        return [x.time_elapsed for x in trades]
    elif want == 'start_time':
        return [x.start_time for x in trades]
    elif want == 'end_time':
        return [x.end_time for x in trades]
    elif want == 'profit':
        return [x.profit for x in trades]
    else:
        return [x.clientId for x in trades]


# turn_to_trades takes a df in which every row has the same symbol and clientId and returns a group of dfs,
# containing each trade. (A trade being defined below).
def turn_to_trades(df, c):
    pd.options.mode.chained_assignment = None  # default='warn'
    # Firstly putting the df into time order:
    df.loc[:, c.time] = df[c.time].map(lambda a: format_time(a, c) if isinstance(a, str) else a)
    df = df.sort_values(by=c.time)

    # Starting by creating a list for the accumulative shares held:
    signs = [1 if x == c.bot else -1 for x in df[c.botsld]]
    cum_shares_this_trade = np.cumsum(df[c.shares] * signs)

    # Searching for when one trade starts and another ends, by seeing where the cumulative number held is 0:
    df = df.reset_index()
    l = df.index[cum_shares_this_trade == 0].tolist()
    l = [x + 1 for x in l]
    l_mod = [0] + l + [max(l) + 1]
    list_of_dfs = [df.iloc[l_mod[n]:l_mod[n + 1]] for n in range(len(l_mod) - 1)]
    list_of_dfs = list(filter(lambda x: not x.empty, list_of_dfs))

    # account for the fact we ONLY want positions that are not still open:
    cum_shares_this_trade = cum_shares_this_trade.reset_index()
    if cum_shares_this_trade[c.shares][len(cum_shares_this_trade) - 1] != 0:
        list_of_dfs = list_of_dfs[:-1]
    return list_of_dfs


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


# Takes an csv of the right format, and converts it into a list of all the trades.
def csv_to_trades(df, c):
    list_of_trades = []
    groups = df.groupby([c.clientid, c.symbol])
    for name, group in groups:
        for item in turn_to_trades(group, c):
            list_of_trades.append(CompleteTrade(item, c))
    return list_of_trades


def profit_of_winning_trades(trades):
    return np.sum(get_list(trade_filter(trades, True), want='profit'))


def losses_of_losing_trades(trades):
    return np.sum(get_list(trade_filter(trades, False), want='profit'))


def net_of_all_trades(trades):
    return np.sum(get_list(trades, want='profit'))


def std_dvn_trade(trades, winning, statistic='profit'):
    return np.round(np.std(get_list(trade_filter(trades, winning), statistic)), decimals=2)


def expected_trade(trades, winning, statistic='profit'):
    return np.round(np.mean(get_list(trade_filter(trades, winning), statistic)), decimals=2)


config = TradeCsvConfig()
tradess = csv_to_trades(data, config)

print(expected_trade(tradess, True))
