import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def cumulative_profit_graph(trades):
    ordered = time_order(trades)
    profits = get_list(ordered, want='profit')
    times = get_list(ordered, want='end_time')
    cumprofits = np.cumsum(profits)
    plt.ylabel('Cumulative profits, $')
    plt.xlabel('Trade number')
    plt.title('A graph of cumulative profits over time traded')
    plt.bar(range(len(cumprofits)), cumprofits, color='g')

    plt.show()



from TradingClasses import *
from FunctionsForStats import *