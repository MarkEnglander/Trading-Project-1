import numpy as np
import pandas as pd

from TradingClasses import *
from FunctionsForStats import *
from TradeGraphs import *
from TradePDFCreator import *

data = pd.read_csv("order_details_US (1).csv")
config = TradeCsvConfig()

data1 = data.groupby(['OrderRef'])

for name, group in data1:
    get_pdf_of_stats(group, str(name), config)