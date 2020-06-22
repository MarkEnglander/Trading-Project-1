import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


#If cumulative is true, will show cumulative profits, otherwise just marginal.
# Set color to 'r' when showing losses.
def profit_graph(trades, trade_list_name='All Trades', color='g', cumulative=True):
    ordered = time_order(trades)
    profits = get_list(ordered, want='profit')
    times = get_list(ordered, want='end_time')
    cumprofits = np.cumsum(profits)
    plt.ylabel('Cumulative profits, $')
    plt.xlabel('Trade number')
    cumstr = ' cumulative' if cumulative else ''
    plt.title('A graph of' + cumstr + ' profits over time for ' + trade_list_name)
    if cumulative:
        plt.bar(range(len(cumprofits)), cumprofits, color=color)
    else:
        plt.bar(range(len(profits)), profits, color=color)
    plt.show()


# Shows a pie chart of the ratio between wins and losses
def win_loss_pie_chart(trades):
    win_no = len(trade_filter(trades, True))
    loss_no = len(trade_filter(trades, False))
    total = float(win_no + loss_no)
    labels = 'Winning', 'Losing'
    sizes = [np.round(100 * win_no / total, 2), np.round(100 * loss_no / total, 2)]
    explode = (0.1, 0)
    fig1, ax1 = plt.subplots()
    colors = ['g', 'r']
    ax1.pie(sizes, colors= colors, explode = explode, labels = labels, autopct = '%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
    return fig1


from TradingClasses import *
from FunctionsForStats import *