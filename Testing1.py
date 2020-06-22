import numpy as np
import pandas as pd

from TradingClasses import *
from FunctionsForStats import *
from TradeGraphs import *

data = pd.read_csv("order_details_US2.csv")


config = TradeCsvConfig()
tradess = csv_to_trades(data, config)

cumulative_profit_graph(tradess)
print(net_of_all_trades(tradess))