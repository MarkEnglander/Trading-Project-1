import numpy as np
import pandas as pd

from TradingClasses import *
from FunctionsForStats import *

data = pd.read_csv("order_details_US2.csv")


config = TradeCsvConfig()
tradess = csv_to_trades(data, config)

print(expected_trade(tradess, True))